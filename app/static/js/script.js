document
.querySelectorAll(
    "input[type='number']"
)
.forEach(input => {
    input.addEventListener(
        "input",
        function () {
            if (this.value < 0) {
                this.value = "";
            }
        }
    );
});

const form =
document.querySelector("form");

if (form) {

    form.addEventListener(
        "submit",
        function () {

            const btn =
            document.querySelector(
                "button"
            );

            btn.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i> Predicting...';

            btn.disabled = true;
        }
    );

}

const overtime =
document.querySelector(
    "select"
);

if (overtime) {

    overtime.addEventListener(
        "change",
        function () {

            if (
                this.value === "Yes"
            ) {
                this.style.border =
                    "2px solid orange";
            }
            else {
                this.style.border =
                    "2px solid #00c6ff";
            }

        }
    );

}