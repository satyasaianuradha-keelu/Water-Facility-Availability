const mapElement = document.getElementById('facilityMap');
if (mapElement) {
  const facilities = JSON.parse(mapElement.dataset.facilities);
  const focusId = Number(mapElement.dataset.focusId || 0);
  const villageLocations = JSON.parse(mapElement.dataset.villageLocations || '{}');
  const translations = window.jalaTranslations; const areaLabels = translations.area_labels || {}; const villageLabels = translations.village_labels || {}; const facilityLabels = translations.facility_labels || {}; const displayArea = area => areaLabels[area] || area; const displayVillage = village => villageLabels[village] || village; const displayFacility = value => facilityLabels[value] || value;
  const map = L.map(mapElement).setView([16.6823116, 81.1409858], 15);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '&copy; OpenStreetMap contributors' }).addTo(map);
  const markers = new Map();
  let userMarker;
  const markerColors = { available: '#1268b3', partial: '#e5ab27', unavailable: '#d9574e', notWorking: '#293238' };
  const statusKey = facility => facility.status !== 'Functional' ? 'notWorking' : facility.availability === 'Available' ? 'available' : facility.availability === 'Partially Available' ? 'partial' : 'unavailable';
  const statusLabel = facility => facility.status !== 'Functional' ? translations.not_working : facility.availability === 'Available' ? translations.available : facility.availability === 'Partially Available' ? translations.partially_available : translations.not_available;
  const markerIcon = facility => L.divIcon({ className: 'facility-marker', html: `<span style="background:${markerColors[statusKey(facility)]}"><i class="icon-droplet"></i></span>`, iconSize: [30, 30], iconAnchor: [15, 15], popupAnchor: [0, -15] });
  const popup = facility => `<div class="map-popup"><strong>${displayFacility(facility.facility_name)}</strong><span>${displayVillage(facility.village)} · ${displayArea(facility.area)} · ${displayFacility(facility.facility_type)}</span><b class="map-status status-${statusKey(facility)}"><i></i>${statusLabel(facility)}</b><small>${translations.updated}: ${facility.last_updated}</small><a class="button primary direction-button" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination=${facility.latitude},${facility.longitude}"><i class="icon-navigation"></i>${translations.get_directions}</a></div>`;
  const focusFacility = facility => { const marker = markers.get(facility.id); if (marker) { map.setView([facility.latitude, facility.longitude], 16); marker.openPopup(); } };
  const render = (village, area = 'All') => {
    markers.forEach(marker => map.removeLayer(marker)); markers.clear();
    const visible = facilities.filter(facility => (village === 'All' || facility.village === village) && (area === 'All' || facility.area === area));
    visible.forEach(facility => { const marker = L.marker([facility.latitude, facility.longitude], { icon: markerIcon(facility) }).bindPopup(popup(facility)).addTo(map); markers.set(facility.id, marker); });
    const list = document.getElementById('facilityMapList'); list.innerHTML = visible.length ? visible.map(facility => `<button class="map-list-item" data-facility-id="${facility.id}"><span class="list-dot ${statusKey(facility)}"></span><span><strong>${displayFacility(facility.facility_name)}</strong><small>${displayFacility(facility.facility_type)} · ${displayArea(facility.area)}</small></span><b>${statusLabel(facility)}</b><i class="icon-chevron-right"></i></button>`).join('') : `<p class="empty-state">${translations.no_facilities}</p>`;
    list.querySelectorAll('[data-facility-id]').forEach(item => item.addEventListener('click', () => focusFacility(visible.find(facility => facility.id === Number(item.dataset.facilityId)))));
    if (visible.length) map.fitBounds(L.latLngBounds(visible.map(facility => [facility.latitude, facility.longitude])), { padding: [28, 28], maxZoom: 15 });
    else if (villageLocations[village]) map.setView([villageLocations[village].latitude, villageLocations[village].longitude], 13);
  };
  const villageSelect = document.getElementById('villageSelect');
  const areaSelect = document.getElementById('areaSelect');
  const villageSearch = document.getElementById('villageSearch');
  const villageSearchForm = document.getElementById('villageSearchForm');
  const villageSuggestions = document.getElementById('villageSuggestions');
  const villageSearchMessage = document.getElementById('villageSearchMessage');
  const areasByVillage = JSON.parse(areaSelect.dataset.areas);
  const villageOptions = [...villageSelect.options].map(option => ({ value: option.value, label: option.textContent, rawLabel: option.dataset.rawLabel || option.textContent }));
  const updateSuggestions = value => {
    const search = value.trim().toLowerCase();
    const matches = villageOptions.filter(option => option.value !== 'All' && (option.label.toLowerCase().includes(search) || option.rawLabel.toLowerCase().includes(search)));
    villageSuggestions.innerHTML = search && matches.length ? matches.map(option => `<button type="button" data-village="${option.value}">${option.label}</button>`).join('') : '';
    villageSuggestions.querySelectorAll('[data-village]').forEach(item => item.addEventListener('click', () => { villageSearch.value = item.dataset.village; villageSearchForm.requestSubmit(); }));
  };
  villageSearch.addEventListener('input', event => {
    const search = event.target.value.trim().toLowerCase();
    const matches = villageOptions.filter(option => option.value === 'All' || (option.label.toLowerCase().includes(search) || option.rawLabel.toLowerCase().includes(search)));
    villageSelect.innerHTML = matches.map(option => `<option value="${option.value}">${option.label}</option>`).join('');
    updateSuggestions(event.target.value);
  });
  villageSearchForm.addEventListener('submit', event => {
    event.preventDefault();
    const search = villageSearch.value.trim().toLowerCase();
    const match = villageOptions.find(option => option.value !== 'All' && (option.label.toLowerCase() === search || option.rawLabel.toLowerCase() === search)) || villageOptions.find(option => option.value !== 'All' && (option.label.toLowerCase().includes(search) || option.rawLabel.toLowerCase().includes(search)));
    if (!match) { villageSearchMessage.textContent = translations.village_not_found || 'Village not found. Please check the spelling and try again.'; villageSearchMessage.className = 'search-message error'; return; }
    villageSearch.value = match.label; villageSelect.innerHTML = villageOptions.map(option => `<option value="${option.value}">${option.label}</option>`).join(''); villageSelect.value = match.value; villageSelect.dispatchEvent(new Event('change')); villageSearchMessage.textContent = `${translations.village_found_prefix || 'Village'} ${match.label} ${translations.village_found_suffix || 'found. Showing water facilities.'}`; villageSearchMessage.className = 'search-message success'; villageSuggestions.innerHTML = '';
  });
  villageSelect.addEventListener('change', event => {
    const areas = areasByVillage[event.target.value] || [];
    areaSelect.innerHTML = `<option value="All">${translations.all_areas}</option>` + areas.map(area => `<option value="${area}">${displayArea(area)}</option>`).join('');
    areaSelect.disabled = event.target.value === 'All';
    render(event.target.value, 'All');
  });
  areaSelect.addEventListener('change', event => render(villageSelect.value, event.target.value));
  document.getElementById('locateButton').addEventListener('click', () => {
    if (!navigator.geolocation) { document.getElementById('locationMessage').textContent = translations.location_unsupported; return; }
    document.getElementById('locationMessage').textContent = translations.locating;
    navigator.geolocation.getCurrentPosition(position => { const { latitude, longitude } = position.coords; if (userMarker) userMarker.remove(); userMarker = L.circleMarker([latitude, longitude], { radius: 9, color: '#1268b3', fillColor: '#6db6e8', fillOpacity: .9 }).addTo(map).bindPopup(translations.your_location).openPopup(); map.setView([latitude, longitude], 15); document.getElementById('locationMessage').textContent = translations.location_found; }, () => { document.getElementById('locationMessage').textContent = translations.location_denied; });
  });
  areaSelect.disabled = true;
  render('All', 'All');
  if (focusId) {
    const target = facilities.find(facility => facility.id === focusId);
    if (target) focusFacility(target);
  }
}
