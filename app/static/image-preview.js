document.getElementById("image").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgPreview = document.getElementById("image-preview");
            imgPreview.src = e.target.result;
            imgPreview.style.display = "block";
        }
        reader.readAsDataURL(file);
    }
});

// Code from ChatGPT