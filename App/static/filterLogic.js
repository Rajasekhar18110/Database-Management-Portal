document.querySelectorAll('.dropdown').forEach(dropdown => {
    dropdown.addEventListener('change', filterTable);
});

function filterTable() {
    const selectedFilters = {
        MetricName: document.getElementById('dropdown-1').value.toLowerCase(),
        DataType: document.getElementById('dropdown-2').value.toLowerCase(),
        EditUser: document.getElementById('dropdown-3').value.toLowerCase(),
    };

    const rows = document.querySelectorAll('#table-body tr');

    rows.forEach(row => {
        const MetricNameValue = row.children[0].textContent.toLowerCase().trim(); // First column (index 0)
        const DataTypeValue = row.children[2].textContent.toLowerCase().trim(); // Second column (index 1)
        const EditUserValue = row.children[9].textContent.toLowerCase().trim(); // Third column (index 2)


        const matchesMetricName = selectedFilters.MetricName === 'all' || MetricNameValue === selectedFilters.MetricName;
        const matchesDataType = selectedFilters.DataType === 'all' || DataTypeValue === selectedFilters.DataType;
        const matchesEditUser = selectedFilters.EditUser === 'all' || EditUserValue === selectedFilters.EditUser;
        console.log('MetricName:' ,MetricNameValue, 'DataType:' ,DataTypeValue, 'EditUser:',EditUserValue);
        console.log('Selected Filters:', selectedFilters);


        if (matchesMetricName && matchesDataType && matchesEditUser) {
            row.style.display = ''; // Show the row
        } else {
            row.style.display = 'none'; // Hide the row
        }
    });
}
