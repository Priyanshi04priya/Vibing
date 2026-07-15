"use client";

import { motion } from 'framer-motion';
import { Compass, Sparkles, MapPin, ShieldCheck, Plane } from 'lucide-react';
import { useState } from 'react';

const highlights = [
  'Mood-based itinerary generation',
  'Budget-aware weekend planning',
  'Hidden-food and hidden-gem discovery',
  'Packing, safety, and story generation',
];

export default function HomePage() {
  const [prompt, setPrompt] = useState("I am tired after exams. Budget ₹2500. Need a one day trip from Delhi. We are four friends. Need peaceful places with good food.");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/plans/compose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, preferences: { budget: 2500, start_city: 'Delhi', companions: 4, mood: 'restorative' } }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      setResult({ title: 'Planner unavailable', summary: 'The backend is not running yet.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto flex min-h-screen max-w-7xl flex-col px-6 py-10 lg:px-10">
      <nav className="mb-16 flex items-center justify-between rounded-full border border-white/10 bg-white/5 px-5 py-3 backdrop-blur-xl">
        <div className="flex items-center gap-3 text-lg font-semibold">
          <div className="rounded-full bg-gradient-to-br from-aurora to-coral p-2">
            <Compass className="h-5 w-5" />
          </div>
          VibeTrip AI
        </div>
      </nav>

      <section className="grid items-center gap-12 lg:grid-cols-[1fr_1fr]">
        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-aurora/30 bg-aurora/10 px-3 py-1 text-sm text-aurora">
            <Sparkles className="h-4 w-4" />
            Plan experiences, not trips.
          </div>
          <h1 className="max-w-3xl text-5xl font-semibold tracking-tight text-white sm:text-6xl">
            Turn your mood into a weekend that feels cinematic.
          </h1>
          <p className="mt-6 max-w-2xl text-lg text-white/70">
            Describe your energy, budget, and vibe. VibeTrip AI assembles an itinerary with food, hidden gems, weather guidance, packing, safety, and a story-ready summary.
          </p>
        </motion.div>

        <motion.div initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6 }} className="rounded-3xl border border-white/10 bg-white/10 p-6 shadow-2xl shadow-aurora/10 backdrop-blur-2xl">
          <div className="mb-4 flex items-center gap-3">
            <div className="rounded-full bg-mint/15 p-3 text-mint">
              <Plane className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm text-white/60">AI planner</p>
              <p className="text-xl font-semibold">Tell the system your vibe</p>
            </div>
          </div>

          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={6}
            className="w-full rounded-2xl border border-white/10 bg-midnight/60 p-4 text-sm text-white/80 outline-none"
          />

          <button
            onClick={handleSubmit}
            className="mt-4 rounded-full bg-white px-5 py-3 font-medium text-midnight"
          >
            {loading ? 'Planning...' : 'Generate experience'}
          </button>

          {result && (
            <div className="mt-6 rounded-2xl border border-white/10 bg-midnight/50 p-4">
              <h2 className="text-lg font-semibold">{result.title}</h2>
              <p className="mt-2 text-sm text-white/70">{result.summary}</p>
              <div className="mt-4 flex items-center gap-2 text-sm text-mint">
                <MapPin className="h-4 w-4" /> {result.destination}
              </div>
              <div className="mt-4 space-y-2">
                {result.itinerary?.map((step: any, index: number) => (
                  <div key={`${step.time}-${index}`} className="rounded-xl border border-white/10 bg-white/5 p-3 text-sm">
                    <div className="font-medium">{step.time} • {step.title}</div>
                    <div className="mt-1 text-white/70">{step.description}</div>
                  </div>
                ))}
              </div>
              <div className="mt-4 rounded-xl border border-white/10 bg-white/5 p-3 text-sm text-white/70">
                <div><span className="font-medium text-white">Memory:</span> {result.memory_summary || 'No memory yet'}</div>
                <div className="mt-2"><span className="font-medium text-white">Hidden gems:</span> {result.hidden_gems?.join(', ')}</div>
                <div className="mt-2"><span className="font-medium text-white">Food picks:</span> {result.food_recommendations?.join(' • ')}</div>
              </div>
            </div>
          )}
        </motion.div>
      </section>

      <section className="mt-12 grid gap-4 md:grid-cols-3">
        {highlights.map((item) => (
          <div key={item} className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white/80">
            <ShieldCheck className="h-4 w-4 text-mint" />
            {item}
          </div>
        ))}
      </section>
    </main>
  );
}
