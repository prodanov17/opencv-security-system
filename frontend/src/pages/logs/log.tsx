import { useRef, useEffect } from "react";
import { Link } from "react-router-dom";

function Log({ onClick, url, date, name }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const video = videoRef.current;

    video.addEventListener("loadeddata", () => {
      // You can adjust the time if you want to capture a frame other than the first one
      video.currentTime = 1;
    });

    video.addEventListener("seeked", () => {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    });
  }, [url]);

  return (
    <Link to={url} onClick={onClick} className=" block flex bg-white rounded-lg gap-4 items-center overflow-hidden">
      <video ref={videoRef} src={url} style={{ display: "none" }}></video>
      <canvas ref={canvasRef} width="100" height="100"></canvas>
      <div className="">
        <h4 className="font-light text-neutral-400 text-xs uppercase">{name}</h4>
        <h3 className="font-semibold">Motion Detected!</h3>
        <p>{new Date(date).toLocaleString()}</p>
      </div>
    </Link>
  );
}

export default Log;
