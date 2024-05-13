document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission behavior

    // Get the selected user type
    var userType = document.getElementById("user_type").value;

    // Redirect to the appropriate page based on the selected user type
    switch(userType) {
        case "student":
            window.location.href = "stuloginfinal.html";
            break;
        case "admin":
            window.location.href = "adminlogin.html";
            break;
        case "company":
            window.location.href = "complogin.html";
            break;
        default:
            // Handle unexpected cases
            console.error("Unexpected user type");
            break;
    }
});