var websocket;

window.addEventListener("DOMContentLoaded", (ev) => {
    
    console.log("load dom", ev);
    websocket = new WebSocket("ws://localhost:5678/");

    console.log("crated socket", websocket)
    var inc = 0
    websocket.onmessage = ({ data }) => {
       
        inc = inc + 1
        if (inc%2 == 0){
            document.getElementById('buttontochange').className = 'formatForButton2';
        }else{
            document.getElementById('buttontochange').className = 'formatForButton';
        }
        
      
    };
  });


window.addEventListener("unload", (ev) => {
    console.log("unload dom", ev);
    if(websocket.readyState == WebSocket.OPEN){
        console.log("closed conection");
        websocket.close();
    }
    
});