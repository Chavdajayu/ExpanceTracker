document.getElementById('expense-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const description = document.getElementById('description').value;
    const amount = document.getElementById('amount').value;
    const category = document.getElementById('category').value;
    const date = document.getElementById('date').value;

    const response = await fetch('/add_expense', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `description=${description}&amount=${amount}&category=${category}&date=${date}`
    });

    if (response.ok) {
        loadExpenses();
        document.getElementById('expense-form').reset();
    }
});

async function loadExpenses() {
    const response = await fetch('/get_expenses');
    const expenses = await response.json();

    const expenseList = document.getElementById('expense-list');
    expenseList.innerHTML = '';  // Clear the existing list

    expenses.forEach((expense, index) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <div class="expense-details">
                <div>${index + 1}</div>
                <div>${expense[1]}</div>  <!-- description -->
                <div>$${expense[2].toFixed(2)}</div>  <!-- amount -->
                <div>${expense[3]}</div>  <!-- category -->
                <div>${expense[4]}</div>  <!-- date -->
            </div>
        `;
        expenseList.appendChild(li);
    });
}

// Load expenses when the page loads
window.onload = loadExpenses;
document.getElementById('download-pdf').addEventListener('click', function() {
    window.location.href = '/download_pdf';
});
