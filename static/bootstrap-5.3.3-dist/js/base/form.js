document.addEventListener('DOMContentLoaded', function() {
    // Username ইনপুট ফিল্ডের জন্য কী ইভেন্ট হ্যান্ডলার
    var usernameInput = document.getElementById('form2Example1');

    // Enter চাপলে পাসওয়ার্ড ফিল্ডে ফোকাস যাবে
    usernameInput.addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
            event.preventDefault();  // ডিফল্ট সাবমিট বন্ধ
            document.getElementById('form2Example2').focus();  // পাসওয়ার্ড ফিল্ডে ফোকাস
        }
    });
});