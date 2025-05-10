
document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('map')) return;
    const coords = [43.022377, 44.412135];
    const map = L.map('map').setView(coords, 15);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    L.marker(coords)
      .addTo(map)
      .bindPopup('Место пока не определено.')
      .openPopup();

  try {
    const mapElement = document.getElementById('map');
    const xpath = '//*[@id="map"]/div[2]/div[4]';

    const element = document.evaluate(
      xpath,
      document,
      null,
      XPathResult.FIRST_ORDERED_NODE_TYPE,
      null
    ).singleNodeValue;

    if (element) {
      element.remove();
    }
  } catch (error) {
    console.error(error);
  }
});