import { howItWorks } from "../content/project";

const { diagram } = howItWorks;

// Layout in SVG user units. The drawing scales to its container.
const WIDTH = 340;
const BOX_H = 88;
const GAP = 40;
const NOTE_H = 64;
const boxY = (index: number) => 8 + index * (BOX_H + GAP);
const noteY = boxY(diagram.boxes.length) - GAP / 2;
const HEIGHT = noteY + NOTE_H + 8;

export function SystemDiagram() {
  return (
    <svg
      role="img"
      aria-labelledby="diagram-title diagram-desc"
      viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
      className="h-auto w-full max-w-md text-ink"
    >
      <title id="diagram-title">{diagram.title}</title>
      <desc id="diagram-desc">{diagram.description}</desc>
      <defs>
        <marker
          id="diagram-arrow"
          viewBox="0 0 10 10"
          refX="5"
          refY="5"
          markerWidth="7"
          markerHeight="7"
          orient="auto"
        >
          <path d="M0 0 10 5 0 10z" fill="var(--accent)" />
        </marker>
      </defs>

      {diagram.boxes.map((box, index) => {
        const y = boxY(index);
        return (
          <g key={box.title}>
            <rect
              x="4"
              y={y}
              width={WIDTH - 8}
              height={BOX_H}
              rx="8"
              fill="var(--surface)"
              stroke="var(--ink)"
              strokeWidth="2"
            />
            <circle cx="36" cy={y + BOX_H / 2} r="16" fill="var(--accent)" />
            <text
              x="36"
              y={y + BOX_H / 2 + 6}
              textAnchor="middle"
              fontSize="17"
              fontWeight="700"
              fill="var(--accent-ink)"
            >
              {index + 1}
            </text>
            <text x="66" y={y + 32} fontSize="18" fontWeight="700" fill="currentColor">
              {box.title}
            </text>
            {box.lines.map((line, lineIndex) => (
              <text key={line} x="66" y={y + 56 + lineIndex * 19} fontSize="15" fill="var(--muted)">
                {line}
              </text>
            ))}
            {index < diagram.boxes.length - 1 ? (
              <line
                x1={WIDTH / 2}
                y1={y + BOX_H + 2}
                x2={WIDTH / 2}
                y2={y + BOX_H + GAP - 6}
                stroke="var(--accent)"
                strokeWidth="3"
                markerEnd="url(#diagram-arrow)"
              />
            ) : null}
          </g>
        );
      })}

      <rect
        x="4"
        y={noteY}
        width={WIDTH - 8}
        height={NOTE_H}
        rx="8"
        fill="none"
        stroke="var(--control)"
        strokeWidth="2"
        strokeDasharray="6 5"
      />
      {diagram.caneNote.map((line, index) => (
        <text
          key={line}
          x={WIDTH / 2}
          y={noteY + 27 + index * 20}
          textAnchor="middle"
          fontSize="16"
          fill="currentColor"
        >
          {line}
        </text>
      ))}
    </svg>
  );
}
