import { SwitchDemo } from "@/ui/shad/Switch";
import React, { useState, useEffect } from "react";

function Feed() {
  const [isLive, setIsLive] = useState(true);
  const [armed, setArmed] = useState(false);

  useEffect(() => {
    const checkArmedStatus = async () => {
      try {
        const response = await fetch("http://localhost:5001/get-armed", {
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
        const response = await fetch("http://localhost:5001/video_feed", {
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
        res = await fetch("http://localhost:5001/arm", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ algorithm: "ml" }),
        });
      } else {
        res = await fetch("http://localhost:5001/disarm", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ algorithm: "ml" }),
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
        <div className="w-full max-w-2xl">
          <div className="flex justify-between items-center px-4">
            <h1 className="text-center text-2xl font-bold mb-4">Live Stream</h1>
              <SwitchDemo
                armed={armed}
                label="Armed"
                callback={handleArmedChange}
              />
          </div>
          <div className="relative pb-9/16 rounded-lg overflow-hidden">
            <img
              className="w-full h-full"
              src="http://localhost:5001/video_feed"
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
