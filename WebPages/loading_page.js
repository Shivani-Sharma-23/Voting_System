document.addEventListener("DOMContentLoaded", function() {
    // Delay the loading circle for 10 seconds (10000 milliseconds)
    setTimeout(function() {
        document.querySelector('.loading-overlay').style.display = 'none';
        document.querySelector('.loading-page').classList.add('active'); // Add this line
    }, 10000); // 10000 milliseconds (10 seconds)

    // Delay the logo arrival for 30 seconds after the loading circle disappears
    setTimeout(function() {
        // Show the logo container
        document.querySelector('.logo-container').classList.add('active');
    }, 30000); // 30000 milliseconds (30 seconds)

    // Logo click event to navigate to another webpage
    document.querySelector('.logo').addEventListener('click', function() {
        // Replace 'destination.html' with the actual destination page
        window.location.href = 'index.html';
    });
});
