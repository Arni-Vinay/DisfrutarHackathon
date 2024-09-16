window.onload = function() {
    let todos = document.querySelectorAll('li');
    todos.forEach(todo => {
        let reminder = todo.innerText.split(" - ")[1];
        if (reminder) {
            let reminderDate = new Date(reminder);
            let now = new Date();

            if (reminderDate > now) {
                let timeout = reminderDate - now;
                setTimeout(() => {
                    alert(`Reminder: ${todo.innerText.split(" - ")[0]}`);
                }, timeout);
            }
        }
    });
};
