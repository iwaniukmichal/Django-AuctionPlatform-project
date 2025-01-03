const background = document.getElementById('background');

function createSymbol() {
    const symbol = document.createElement('div');
    symbol.classList.add('symbol');
    const randomNumber = Math.floor(Math.random() * 1000);
    symbol.innerText = `$${randomNumber}`;
    symbol.style.left = `${Math.random() * window.innerWidth}px`;
    symbol.style.top = `${Math.random() * window.innerHeight}px`;
    symbol.style.animationDuration = `${Math.random() * 10 + 5}s`;
    symbol.style.fontSize = `${Math.random() * 3 + 0.5}rem`;
    background.appendChild(symbol);

    setTimeout(() => {
        symbol.remove();
    }, 10000);
}

setInterval(createSymbol, 400);
