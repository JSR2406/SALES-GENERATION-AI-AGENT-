"use strict";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold tracking-tight"
        >
          Sales.AI Pipeline
        </motion.h1>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
         <motion.div 
           whileHover={{ scale: 1.05 }}
           className="glass p-8 rounded-2xl"
         >
            <h2 className="text-xl font-semibold mb-4">Autonomous Agents</h2>
            <p className="text-white/60">LangGraph is prospecting new leads in the background.</p>
         </motion.div>
      </div>
    </main>
  );
}
