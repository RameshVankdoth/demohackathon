$(document).ready(function() {
    function updateCityDropdown(stateSelector, citySelector) {
        var stateId = stateSelector.val();
        if (!stateId) {
            citySelector.html('<option value="" disabled selected>Select City</option>');
            return;
        }
        $.getJSON("{{ url_for('get_cities') }}", { state_id: stateId }, function(data) {
            citySelector.html('<option value="" disabled selected>Select City</option>');
            $.each(data.cities, function(index, city) {
                citySelector.append($('<option>', {
                    value: city.id,
                    text: city.name
                }));
            });
        });
    }

    $('#homeState').change(function() {
        updateCityDropdown($(this), $('#homeCity'));
    });

    $('#currState').change(function() {
        updateCityDropdown($(this), $('#currCity'));
    });
});



var cities = {{ cities|tojson|safe }};
var states = {{ states|tojson|safe }};

function updateCityDropdown(stateSelectId, citySelectId) {
    var stateId = document.getElementById(stateSelectId).value;
    var citySelect = document.getElementById(citySelectId);
    
    // Clear previous options
    citySelect.innerHTML = '<option value="">Select City</option>';

    // Filter and add new options
    cities.forEach(function(city) {
        if (city.state_id == stateId) {
            var option = document.createElement('option');
            option.value = city.id;
            option.textContent = city.name;
            citySelect.appendChild(option);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    var stateSelect = document.getElementById('homeState');
    stateSelect.addEventListener('change', function() {
        updateCityDropdown('homeState', 'homeCity');
    });

    // Trigger the update function on page load if a state is pre-selected
    updateCityDropdown('homeState', 'homeCity');
});

document.addEventListener('DOMContentLoaded', function() {
    var stateSelect = document.getElementById('currState');
    stateSelect.addEventListener('change', function() {
        updateCityDropdown('currState',  'currCity');
    });

    // Trigger the update function on page load if a state is pre-selected
    updateCityDropdown('currState', 'currCity');
});



function validatePassword() {
    var password = document.getElementById('Password').value;
    var confirmPassword = document.getElementById('Conpass').value;
    var validationMessage = "";
    var isValid = true;

    // Check the length of the password
    if (password.length < 8) {
        validationMessage += "Password must be at least 8 characters long<br>";
        isValid = false;
    } else if (password.length > 12) {
        validationMessage += "Password must not exceed 12 characters<br>";
        isValid = false;
    }

    // Check for uppercase letter
    if (!/[A-Z]/.test(password)) {
        validationMessage += "Password must contain at least one uppercase letter<br>";
        isValid = false;
    }

    // Check for lowercase letter
    if (!/[a-z]/.test(password)) {
        validationMessage += "Password must contain at least one lowercase letter<br>";
        isValid = false;
    }

    // Check for digit
    if (!/\d/.test(password)) {
        validationMessage += "Password must contain at least one digit<br>";
        isValid = false;
    }

    // Check for special character
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        validationMessage += "Password must contain at least one special character<br>";
        isValid = false;
    }

    // Check if passwords match
    if (password !== confirmPassword) {
        validationMessage += "Passwords do not match<br>";
        isValid = false;
    }

    // Display validation message
    var passCheck = document.getElementById('pass-check');
    passCheck.innerHTML = validationMessage;

    // Return false to prevent form submission if invalid
    return isValid;
}

function togglePassword(id) {
    var input = document.getElementById(id);
    var toggleIcon = document.querySelector(`#${id} ~ .toggle-password i`);

    if (input.type === 'password') {
        input.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// Attach event listeners to validate password on input
document.getElementById('Password').addEventListener('input', validatePassword);
document.getElementById('Conpass').addEventListener('input', validatePassword);


function myFunction() {
    var x = document.getElementById("myTopnav");
    var overlay = document.getElementById("overlay");
    
    if (x.className === "topnav") {
        x.className += " responsive";
        overlay.style.display = "block"; // Show the overlay
    } else {
        x.className = "topnav";
        overlay.style.display = "none"; // Hide the overlay
    }
}

// Close the menu and overlay when clicking on the overlay
document.getElementById("overlay").addEventListener("click", function() {
    var x = document.getElementById("myTopnav");
    x.className = "topnav";
    this.style.display = "none"; // Hide the overlay
});