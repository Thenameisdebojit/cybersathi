import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import logoImage from "figma:asset/71aa75a51c83ada1205fee5b9fae50fb3843bb55.png";

export default function App() {
  const [animationPhase, setAnimationPhase] = useState<"logo" | "zoom" | "complete">("logo");

  useEffect(() => {
    // Logo appears and stays for 1.5 seconds
    const logoTimer = setTimeout(() => {
      setAnimationPhase("zoom");
    }, 1500);

    return () => clearTimeout(logoTimer);
  }, []);

  useEffect(() => {
    // After zoom animation completes, set to complete
    if (animationPhase === "zoom") {
      const zoomTimer = setTimeout(() => {
        setAnimationPhase("complete");
      }, 2000);

      return () => clearTimeout(zoomTimer);
    }
  }, [animationPhase]);

  return (
    <div className="relative w-screen h-screen bg-[#0a0e27] overflow-hidden">
      {/* Animated background particles */}
      <div className="absolute inset-0">
        {[...Array(30)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-[#00D9FF] rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              opacity: [0, 1, 0],
              scale: [0, 1.5, 0],
            }}
            transition={{
              duration: 2 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>

      {/* Subtle grid background */}
      <motion.div 
        className="absolute inset-0 opacity-10"
        animate={animationPhase === "zoom" ? { opacity: 0 } : {}}
        transition={{ duration: 0.5 }}
      >
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `
              linear-gradient(#00D9FF 1px, transparent 1px),
              linear-gradient(90deg, #00D9FF 1px, transparent 1px)
            `,
            backgroundSize: '60px 60px',
          }}
        />
      </motion.div>

      {/* Radial glow effect */}
      <motion.div
        className="absolute inset-0"
        style={{
          background: 'radial-gradient(circle at center, rgba(0, 217, 255, 0.15) 0%, transparent 60%)',
        }}
        animate={{
          opacity: animationPhase === "zoom" ? 0 : [0.3, 0.6, 0.3],
        }}
        transition={{
          duration: 2,
          repeat: animationPhase === "zoom" ? 0 : Infinity,
          ease: "easeInOut",
        }}
      />

      {/* Main logo animation container */}
      <div className="absolute inset-0 flex items-center justify-center">
        <AnimatePresence>
          {animationPhase !== "complete" && (
            <motion.div
              className="relative"
              initial={{ scale: 0, opacity: 0, rotate: -180 }}
              animate={{
                scale: animationPhase === "logo" ? [0, 1.2, 1] : [1, 3.5],
                opacity: animationPhase === "logo" ? [0, 1, 1] : [1, 1],
                rotate: animationPhase === "logo" ? [-180, 0] : [0, 0],
              }}
              transition={{
                duration: animationPhase === "logo" ? 1.2 : 1.5,
                ease: animationPhase === "logo" ? [0.34, 1.56, 0.64, 1] : "easeInOut",
              }}
            >
              {/* Logo image */}
              <motion.img
                src={logoImage}
                alt="CyberSathi Logo"
                className="w-80 h-80 object-contain"
                style={{
                  filter: "drop-shadow(0 0 30px rgba(0, 217, 255, 0.6))",
                }}
              />

              {/* Glow effect behind logo */}
              <motion.div
                className="absolute inset-0 blur-2xl"
                animate={{
                  opacity: [0.4, 0.8, 0.4],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
              >
                <img
                  src={logoImage}
                  alt=""
                  className="w-80 h-80 object-contain opacity-60"
                />
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Keyhole zoom overlay - creates the effect of zooming through the keyhole */}
        <AnimatePresence>
          {animationPhase === "zoom" && (
            <motion.div
              className="absolute inset-0 flex items-center justify-center pointer-events-none"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {/* Circular vignette that grows */}
              <motion.div
                className="absolute inset-0 bg-black"
                style={{
                  maskImage: 'radial-gradient(circle at center, transparent 0%, black 100%)',
                  WebkitMaskImage: 'radial-gradient(circle at center, transparent 0%, black 100%)',
                }}
                initial={{ 
                  maskSize: '200% 200%',
                  WebkitMaskSize: '200% 200%',
                }}
                animate={{ 
                  maskSize: '20% 20%',
                  WebkitMaskSize: '20% 20%',
                }}
                transition={{ duration: 1.5, ease: "easeInOut" }}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* CyberSathi text */}
      <AnimatePresence>
        {animationPhase === "logo" && (
          <motion.div
            className="absolute inset-0 flex items-center justify-center pointer-events-none"
            initial={{ opacity: 0, y: 100 }}
            animate={{ opacity: [0, 1], y: [100, 0] }}
            exit={{ opacity: 0, y: -50 }}
            transition={{
              duration: 0.8,
              delay: 0.8,
            }}
          >
            <div className="text-center mt-96 pt-32">
              <motion.h1
                className="text-[#00D9FF] tracking-[0.4em] mb-3"
                animate={{
                  textShadow: [
                    "0 0 10px rgba(0, 217, 255, 0.5)",
                    "0 0 20px rgba(0, 217, 255, 0.8)",
                    "0 0 10px rgba(0, 217, 255, 0.5)",
                  ],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
              >
                CYBERSATHI
              </motion.h1>
              <div className="flex items-center justify-center gap-2">
                {[0, 1, 2].map((i) => (
                  <motion.div
                    key={i}
                    className="w-2 h-2 bg-[#00D9FF] rounded-full"
                    animate={{
                      opacity: [0.3, 1, 0.3],
                      scale: [1, 1.3, 1],
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      delay: i * 0.2,
                    }}
                  />
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Circular scan lines */}
      <AnimatePresence>
        {animationPhase === "logo" && (
          <>
            {[...Array(3)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-[#00D9FF]"
                style={{
                  width: "400px",
                  height: "400px",
                }}
                initial={{ scale: 1, opacity: 0 }}
                animate={{
                  scale: [1, 2.5],
                  opacity: [0.6, 0],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  delay: i * 0.7,
                  ease: "easeOut",
                }}
              />
            ))}
          </>
        )}
      </AnimatePresence>

      {/* Final black screen */}
      <motion.div
        className="absolute inset-0 bg-black pointer-events-none"
        initial={{ opacity: 0 }}
        animate={{
          opacity: animationPhase === "complete" ? 1 : 0,
        }}
        transition={{ duration: 0.5 }}
      />

      {/* Corner accents */}
      <AnimatePresence>
        {animationPhase === "logo" && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.6 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
          >
            {/* Top left */}
            <div className="absolute top-8 left-8 w-12 h-12 border-t-2 border-l-2 border-[#00D9FF]" />
            {/* Top right */}
            <div className="absolute top-8 right-8 w-12 h-12 border-t-2 border-r-2 border-[#00D9FF]" />
            {/* Bottom left */}
            <div className="absolute bottom-8 left-8 w-12 h-12 border-b-2 border-l-2 border-[#00D9FF]" />
            {/* Bottom right */}
            <div className="absolute bottom-8 right-8 w-12 h-12 border-b-2 border-r-2 border-[#00D9FF]" />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
