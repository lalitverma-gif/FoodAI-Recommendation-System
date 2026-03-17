// -----------------------------
// View Restaurant Details
// -----------------------------
function viewRestaurant(name) {
    // Navigates securely to the SPECIFIC static detail pages you requested
    if (name === "Pizza Palace") {
        window.location.href = "/pizza_palace";
    } else if (name === "Burger Hub") {
        window.location.href = "/burger_hub";
    } else if (name === "Cafe Aroma") {
        window.location.href = "/cafe_aroma";
    } else if (name === "Pizza Hut") {
        window.location.href = "/pizza_hut";
    } else if (name === "Dominos") {
        window.location.href = "/dominos";
    } else {
        window.location.href = "/restaurant/" + encodeURIComponent(name);
    }
}

// -----------------------------
// Search Restaurant
// -----------------------------
function searchRestaurant() {
    let query = document.getElementById("searchInput").value;

    if (query === "") {
        alert("Please enter search text");
        return;
    }

    fetch("/search?query=" + encodeURIComponent(query))
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                alert("No restaurants found");
                return;
            }

            let results = "Results:\n";
            data.forEach(r => {
                results += r.name + " (" + r.category + ")\n";
            });

            alert(results);
        })
        .catch(error => console.error("Error searching:", error));
}

// -----------------------------
// Rate Restaurant
// -----------------------------
function rateRestaurant(business_id, rating, user_id) {
    fetch("/rate_business", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            user_id: user_id,
            business_id: business_id,
            rating: rating
        })
    })
        .then(response => response.json())
        .then(data => {
            alert("Rating submitted! " + data.status);
        })
        .catch(error => console.error("Error rating:", error));
}

// -----------------------------
// AI Chatbot Logic
// -----------------------------
function toggleChat() {
    let chatWindow = document.getElementById("chat-window");
    if (chatWindow.style.display === "none" || chatWindow.style.display === "") {
        chatWindow.style.display = "flex";
    } else {
        chatWindow.style.display = "none";
    }
}

function handleChatEnter(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function sendQuickReply(text) {
    document.getElementById("chat-input").value = text;
    sendMessage();
}

function sendMessage() {
    let inputField = document.getElementById("chat-input");
    let message = inputField.value.trim();

    if (message === "") return;

    // 1. Add User Message to UI
    let chatBody = document.getElementById("chat-body");
    chatBody.innerHTML += `<div class="message user-message">${message}</div>`;
    
    // Clear input
    inputField.value = "";
    
    // Scroll to bottom
    chatBody.scrollTop = chatBody.scrollHeight;

    // 2. Fetch response from Flask Backend
    fetch("/chatbot", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // 3. Add Bot Response to UI
        setTimeout(() => {
            chatBody.innerHTML += `<div class="message bot-message">${data.reply}</div>`;
            chatBody.scrollTop = chatBody.scrollHeight;
        }, 500); // Slight delay for realism
    })
    .catch(error => {
        console.error("Chat Error:", error);
        chatBody.innerHTML += `<div class="message bot-message" style="color: red;">Sorry, I encountered an error.</div>`;
    });
}
