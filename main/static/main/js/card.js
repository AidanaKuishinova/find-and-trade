

document.querySelector('.card-number-input').oninput = () => {
    document.querySelector('.card-num-box').innerText = document.querySelector('.card-number-input').value;
}

document.querySelector('.card-holder-input').oninput = () => {
    document.querySelector('.card-holder-name').innerText = document.querySelector('.card-holder-input').value;
}

document.querySelector('.month-input').oninput = () => {
    document.querySelector('.exp-mm').innerText = document.querySelector('.month-input').value;
}

document.querySelector('.year-input').oninput = () => {
    document.querySelector('.exp-yy').innerText = document.querySelector('.year-input').value;
}

document.querySelector('.cvv-input').onmouseenter = () => {
    document.querySelector('.cardfront').style.transform = 'perspective(1000px) rotateY(-180deg)';
    document.querySelector('.cardback').style.transform = 'perspective(1000px) rotateY(0deg)';
}

document.querySelector('.cvv-input').onmouseleave = () => {
    document.querySelector('.cardfront').style.transform = 'perspective(1000px) rotateY(0deg)';
    document.querySelector('.cardback').style.transform = 'perspective(1000px) rotateY(180deg)';
}

document.querySelector('.cvv-input').oninput = () => {
    document.querySelector('.cvv-box').innerText = document.querySelector('.cvv-input').value
}
