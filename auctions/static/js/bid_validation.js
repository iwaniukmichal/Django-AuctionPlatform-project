const bidData = document.getElementById('bid-data');
const currentBid = parseFloat(bidData.getAttribute('data-current-bid'));
const startingBid = parseFloat(bidData.getAttribute('data-starting-bid'));

const form = document.getElementById('bidForm');
const errorMessage = document.getElementById('error-message');

form.addEventListener('submit', function (event) {
    console.log(currentBid);
    const userBid = parseFloat(document.getElementById('bid_amount').value);

    if (currentBid) {
        if (userBid <= currentBid) {
            event.preventDefault();
            errorMessage.textContent = `Your bid must be higher than the current bid of $${currentBid.toFixed(2)}. Please try again.`;
            errorMessage.style.display = 'block';
        }
    } else if (userBid <= startingBid) {
        event.preventDefault();
        errorMessage.textContent = `Your bid must be higher than the starting bid of $${startingBid.toFixed(2)}. Please try again.`;
        errorMessage.style.display = 'block';
    }
});
