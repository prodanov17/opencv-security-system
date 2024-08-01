import { SwitchDemo } from "@/ui/shad/Switch";
import React, { useState, useEffect } from "react";

function Feed() {
  const [isLive, setIsLive] = useState(true);
  const [armed, setArmed] = useState(false);
  const [algorithm, setAlgorithm] = useState("ml");

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    const checkArmedStatus = async () => {
      try {
        const response = await fetch(API_URL + "/get-armed", {
          method: "GET",
        });

        if (!response.ok) {
          setArmed(false);
        } else {
          const armed = await response.json();
          setArmed(armed.armed);
        }
      } catch (error) {
        setArmed(false);
      } finally {
        setArmed(false);
      }
    };
    const checkStreamStatus = async () => {
      try {
        const response = await fetch(API_URL + "/video_feed", {
          method: "HEAD",
        });

        if (!response.ok) {
          setIsLive(false);
        } else {
          setIsLive(true);
        }
      } catch (error) {
        setIsLive(false);
      }
    };

    checkArmedStatus();
    checkStreamStatus();
    const interval = setInterval(checkStreamStatus, 5000); // Check every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const handleArmedChange = async (checked: boolean) => {
    try {
      let res;

      if (checked) {
        res = await fetch(API_URL + "/arm", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ algorithm: algorithm || "ml" }),
        });
      } else {
        res = await fetch(API_URL + "/disarm", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });
      }

      if (res.ok) {
        console.log("Armed/Disarmed");
      }
      setArmed(checked);
    } catch (error) {
      console.error("Failed to arm/disarm");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      {isLive ? (
        <div className="w-full max-w-2xl flex flex-col gap-4">
          <div className="flex justify-between items-center ">
            <h1 className="text-center text-xl font-bold">Detection method</h1>
            <SwitchDemo
              armed={armed}
              label="Armed"
              callback={handleArmedChange}
            />
          </div>
          <div>
            <select className="w-full p-2 rounded text-neutral-600" value={algorithm} onChange={(e) => setAlgorithm(e.target.value)}>
            <option value="ml">Machine Learning</option>
            <option value="hog">Histogram of gradients</option>
            <option value="mog">Background subtraction</option>
            </select>
          </div>
          <div className="relative pb-9/16 rounded-lg overflow-hidden">
            <img
              className="w-full h-full"
              src={API_URL + "/video_feed"}
              alt="Live Stream"
            />
          </div>
        </div>
      ) : (
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Stream is not live</h1>
          <p className="text-gray-600">Please check back later.</p>
        </div>
      )}
    </div>
  );
}

export default Feed;
