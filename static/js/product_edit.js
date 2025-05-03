function onImageSelected(event) {
  var selectedFile = event.target.files[0];
  var reader = new FileReader();

  var image = document.getElementById("productImage");
  image.title = selectedFile.name;

  reader.onload = function(event) {
    image.src = event.target.result;
  };

  reader.readAsDataURL(selectedFile);
}