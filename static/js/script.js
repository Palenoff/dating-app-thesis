let touchstartX = 0;
let touchendX = 0;
const minSwipeDistance = 50; // Minimum distance for a swipe gesture

function handleSwipe() {
    const profiles = document.getElementsByClassName('inner_profile');

    for (const profile of profiles) {
        profile.addEventListener('touchstart', function(event) {
            touchstartX = event.touches[0].clientX;
        });

        profile.addEventListener('touchend', function(event) {
            touchendX = event.changedTouches[0].clientX;
            handleGesture();
        });
    }
}

function handleGesture() {
    const deltaX = touchendX - touchstartX;

    if (Math.abs(deltaX) > minSwipeDistance) {
        if (deltaX > 0) {
            submitRatings('Previous');
        } else {
            submitRatings('Next');
        }
    }
}

function inputNumberAbs() {
    var input = document.getElementById("age");
    var val = input.value;
    val = val.replace(/^0+|[^\d.]/g, '');
    input.value = val;
  }

function submitRatings(direction){
    var form = document.getElementById('ratings');

        // Append the hidden input to the form
    var hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'to';
    hiddenInput.value = direction;
        // Append the hidden input to the form
    form.appendChild(hiddenInput);
        // Submit the form
    form.submit();
}
// function getProfile(current_profile) {
//     fetch("/profile", {
//         method: "POST",
//         headers: {'Content-Type': 'application/json'}, 
//         body: JSON.stringify({
//             current_profile: current_profile,
//         })
//     })
//     .then(response => response.text())
//     .then(htmlContent => {
//         document.open();
//         document.write(htmlContent);
//         document.close();
//     })
//     .catch(error => console.error('Error:', error));
//   }

// function go_back() {
//     current_n = parseInt(document.querySelector('.profile').id)
//     if (current_n > 0)
//         getProfile(current_n - 1)
// }

// function go_forward() {
//     const current_n = parseInt(document.querySelector('.profile').id)
//     if (current_n > 0)
//         submitRatings(current_n);
//         getProfile(current_n + 1)
//     // fetch("/post/data/here", {
//     // method: "POST",
//     // headers: {'Content-Type': 'application/json'}, 
//     // body: JSON.stringify({"participant_id":data,"current_n":nextProfileId})
//     // }).then(res => {
//     // console.log("Request complete! response:", res);
//     // });
//     // Update the URL to navigate to the next/previous profile
//     // window.location.href = `/profile`;
// }

// function submitRatings(current_n) {
//     const attractiveness = parseInt(document.getElementById('attractiveness').value);
//     const trustworthiness = parseInt(document.getElementById('trustworthiness').value);
//     const authenticity = parseInt(document.getElementById('authenticity').value);

//     // Send an AJAX request to the server with the ratings and profile ID
//     const xhr = new XMLHttpRequest();
//     xhr.open('POST', '/submit_ratings', true);
//     xhr.setRequestHeader('Content-Type', 'application/json');

//     const data = JSON.stringify({
//         current_n: current_n,
//         attractiveness: attractiveness,
//         trustworthiness: trustworthiness,
//         authenticity: authenticity
//     });

//     xhr.send(data);
// }

// function startSwipingTest() {
//     getProfile('0');
//   }

// function createParticipant(preferred_gender) {
//     fetch("/create_participant", {
//         method: "POST",
//         headers: {'Content-Type': 'application/json'}, 
//         body: JSON.stringify({
//             preferred_gender: preferred_gender,
//         })
//     })
//         .then(res => {
//             if (res.ok)
//             {
//                 console.log("Participant created. Profiles generated! response:", res);
//             }
//             else{
//                 console.log(res.text())
//             }
//        });
// }

// function generate_profiles() {
//     fetch("/generate_profiles", {
//     method: "POST",
//     headers: {'Content-Type': 'application/json'}, 
//     body: JSON.stringify({
//         current_profile: '0'
//     })
// })
//     .then(res => {
//         if (res.ok)
//         {
//             console.log("Profiles generation comple! response:", res);
//             getProfile('0');
//         }
//         else{
//             console.log(res.text())
//         }
//    });
//   }


document.addEventListener('DOMContentLoaded', function() {
    handleSwipe();
});