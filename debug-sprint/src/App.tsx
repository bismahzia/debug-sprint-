import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Bug, Rocket, Code2, Zap } from 'lucide-react'

function App() {
  const [level, setLevel] = useState(1)
  const [score, setScore] = useState(0)
  const [bugs, setBugs] = useState([
    {id: 1, text: "Null pointer in line 42", fixed: false},
    {id: 2, text: "Infinite loop in render()", fixed: false},
    {id: 3, text: "API key exposed in frontend", fixed: false},
  ])

  const fixBug = (id: number) => {
    setBugs(bugs.map(b => b.id === id ? {...b, fixed: true} : b))
    setScore(score + 100)
    if (bugs.filter(b => !b.fixed).length === 1) setLevel(level + 1)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0B1020] to-[#1E293B] p-8 font-mono">
      <motion.div initial={{opacity: 0, y: -20}} animate={{opacity: 1, y: 0}} className="max-w-4xl mx-auto">
        <div className="flex items-center gap-3 mb-8">
          <Code2 className="w-8 h-8 text-cyan-400" />
          <h1 className="text-3xl font-bold text-white">Debug Sprint</h1>
          <Zap className="w-6 h-6 text-yellow-400" />
        </div>
        
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-[#1E293B] p-4 rounded-lg border-cyan-500/20">
            <p className="text-gray-400 text-sm">Level</p>
            <p className="text-2xl font-bold text-cyan-400">{level}</p>
          </div>
          <div className="bg-[#1E293B] p-4 rounded-lg border-purple-500/20">
            <p className="text-gray-400 text-sm">Score</p>
            <p className="text-2xl font-bold text-purple-400">{score}</p>
          </div>
          <div className="bg-[#1E293B] p-4 rounded-lg border-green-500/20">
            <p className="text-gray-400 text-sm">Bugs Left</p>
            <p className="text-2xl font-bold text-green-400">{bugs.filter(b => !b.fixed).length}</p>
          </div>
        </div>

        <div className="space-y-3">
          {bugs.map(bug => (
            <motion.div key={bug.id} whileHover={{scale: 1.02}} 
              className={`p-4 rounded-lg border ${bug.fixed ? 'bg-green-900/20 border-green-500/30' : 'bg-[#1E293B] border-red-500/30'}`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Bug className={`w-5 h-5 ${bug.fixed ? 'text-green-400' : 'text-red-400'}`} />
                  <p className={`text-white ${bug.fixed ? 'line-through opacity-50' : ''}`}>{bug.text}</p>
                </div>
                {!bug.fixed && (
                  <button onClick={() => fixBug(bug.id)} className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded-lg text-white text-sm font-bold transition">
                    Fix
                  </button>
                )}
              </div>
            </motion.div>
          ))}
        </div>

        {level > 1 && (
          <motion.div initial={{scale: 0}} animate={{scale: 1}} className="mt-8 text-center">
            <Rocket className="w-16 h-16 mx-auto text-cyan-400 mb-2" />
            <p className="text-xl text-white font-bold">Level Up! You&apos;re a real debugger now 🚀</p>
          </motion.div>
        )}
      </motion.div>
    </div>
  )
}

export default App