
////////////////////////////////
const toastEls = document.getElementsByClassName('alert-dismissible');
if (toastEls) {
    for (let i = 0; i < toastEls.length; i++) {
        const toastEl = toastEls[i];
        if (!toastEl.classList.contains('alert-danger')){
            const timeout = 5000 + 1000*i;
            let timeoutId;
            let startTime;
            let remainingTime = timeout;

            const barreEl = toastEl.querySelector('.barre')
            // console.log(barreEl)
//            if (barreEls.length > 0) {
//                const barreEl = barreEls[0]
//            }

            const handleMouseEnter = () => {
              clearTimeout(timeoutId);
              startTime = Date.now();
            };

            const handleMouseLeave = () => {
              const elapsedTime = Date.now() - startTime;
              remainingTime -= elapsedTime;

              if (remainingTime > 0) {
                timeoutId = setTimeout(() => {
                  toastEl.style.display = 'none';
                }, remainingTime);
              } else {
                toastEl.style.display = 'none';
              }
            };

            const updateTimerDisplay = (elt) => {
                if (elt){
                    elt.style.width = "${remainingTime/timeout}%";
                }
//              const seconds = Math.floor(remainingTime / 1000);
//              timerDisplay.textContent = `(${seconds}s)`;
            };

            const timerInterval = setInterval(() => {
              if (remainingTime > 0) {
                remainingTime -= 100;
                if (barreEl){
                    updateTimerDisplay(barreEl);
                }
              }
            }, 100);

            toastEl.addEventListener('mouseenter', handleMouseEnter);
            toastEl.addEventListener('mouseleave', handleMouseLeave);

            // Start the initial timeout
            timeoutId = setTimeout(() => {
              toastEl.style.display = 'none';
            }, timeout);
        }
    }
}
