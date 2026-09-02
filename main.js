const menuToggle = document.querySelector('[data-menu-toggle]');
const menu = document.querySelector('[data-menu]');
if (menuToggle) menuToggle.addEventListener('click', () => menu.classList.toggle('open'));
const voiceButton = document.getElementById('voiceButton');
if (voiceButton) {
  const description = document.getElementById('description');
  const voiceStatus = document.getElementById('voiceStatus');
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) { voiceStatus.textContent = window.jalaTranslations.voice_unsupported; voiceButton.disabled = true; }
  else {
    const recognition = new SpeechRecognition(); recognition.continuous = true; recognition.interimResults = true;
    recognition.lang = document.documentElement.lang === 'te' ? 'te-IN' : 'en-IN'; let listening = false;
    voiceButton.addEventListener('click', () => { if (listening) recognition.stop(); else recognition.start(); });
    recognition.onstart = () => { listening = true; voiceButton.classList.add('recording'); voiceButton.querySelector('span').textContent = window.jalaTranslations.voice_stop; voiceStatus.textContent = window.jalaTranslations.voice_stop; };
    recognition.onend = () => { listening = false; voiceButton.classList.remove('recording'); voiceButton.querySelector('span').textContent = window.jalaTranslations.voice_start; voiceStatus.textContent = window.jalaTranslations.voice_ready; };
    recognition.onresult = event => { let text = ''; for (let i = event.resultIndex; i < event.results.length; i++) text += event.results[i][0].transcript; if (event.results[event.results.length - 1].isFinal) description.value += (description.value ? ' ' : '') + text.trim(); };
  }
}
