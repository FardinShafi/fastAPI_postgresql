async function getTableColumns() {
    const tableSelect = document.getElementById('table-select');
    const selectedTable = tableSelect.value;

    const columnDetailsDiv = document.getElementById('column-details');
    columnDetailsDiv.innerHTML = '';

    if (selectedTable) {
        try {
            const response = await fetch(`/tables/${selectedTable}/columns`);
            const data = await response.json();

            const columnDetailsHTML = Object.entries(data).map(([columnName, columnType]) => {
                return `<p><strong>${columnName}</strong>: ${columnType}</p>`;
            }).join('');

            columnDetailsDiv.innerHTML = columnDetailsHTML;
        } catch (error) {
            console.error('Error fetching column details:', error);
        }
    }
}

async function populateTableSelect() {
    const tableSelect = document.getElementById('table-select');

    try {
        const response = await fetch('/tables');
        const data = await response.json();

        data.forEach(tableName => {
            const option = document.createElement('option');
            option.text = tableName;
            tableSelect.add(option);
        });
    } catch (error) {
        console.error('Error fetching table names:', error);
    }
}

// Populate table select on page load
populateTableSelect();
