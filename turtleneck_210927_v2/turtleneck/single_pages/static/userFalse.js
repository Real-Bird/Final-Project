// Load the image model and setup the webcam
async function init() {
    const model = await tf.loadLayersModel('https://raw.githubusercontent.com/Real-Bird/pb/master/json/model.json');
        const co_audio = new Audio('https://raw.githubusercontent.com/Real-Bird/pb/master/good_pose.mp3');
        const fo_audio = new Audio('https://raw.githubusercontent.com/Real-Bird/pb/master/bad_pose.mp3');
        let w = 640, h = 480;
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
        let constraints = {audio: false, video: true};
        let video = document.getElementById("videoInput");
        let guideLine = document.getElementById("guideLine");
        video.width = w;
        video.height = h;
        function successCallback(stream){
              video.srcObject = stream;
              video.play();
        }
        function errorCallback(error){
               console.log(error);
        }
        navigator.getUserMedia(constraints, successCallback, errorCallback);
        let canvas = document.getElementById("videoOutput");
        canvas.width = w;
        canvas.height = h;
        ctx = canvas.getContext("2d");
        function processImage(){
            ctx.drawImage(video, 0, 0, w, h);
            ctx.drawImage(guideLine, 130, 120, 420, 360);
            setTimeout(processImage, 1);
            
        }
        processImage();

        function stream(){
            setInterval(sendImage, 30);
        }
        
        // const FPS = 30;
        let count = 0;
        // let d = new Date();
        async function tpredict(){
            
            // let begin = Date.now();
            const webcam = await tf.data.webcam(video, {
            resizeWidth: 224,
            resizeHeight: 224,
            }); 
            // let image = await webcam.capture();
            let image = tf.browser.fromPixels(video)
            image = tf.image.resizeBilinear(image, [224,224])
            image = tf.expandDims(image, 0)
            const out = model.predict(image)
            const predictionArray = out.dataSync()
            const maxValue = predictionArray.valueOf(Math.max(...predictionArray))
            // console.log("val",maxValue[0])
            if (maxValue[0] == 0){
                document.getElementById("label-container").innerHTML = "<strong>corr</strong>";
                
                co_audio.play();
            } else if (maxValue[0] == 1){
                count++;
                document.getElementById("label-container").innerHTML = "<strong>forw</strong>";
                document.getElementById("counter").innerHTML = "<strong>거북목 " + count + " 회</strong>";
                
                fo_audio.play();
            }
            // let now = new Date();

            let delay = 10000 // / FPS - (Date.now() - begin);
            // console.log(now.getSeconds() - d.getSeconds())
            setTimeout(tpredict, delay);
        }   
        // setInterval(tpredict, delay); 
        tpredict();
}