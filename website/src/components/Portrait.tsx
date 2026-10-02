import manifest from "../assets/team/manifest.json";

interface Source {
  file: string;
  width: number;
  height: number;
}

const photos: Record<string, Source[]> = manifest;
const urls = import.meta.glob<string>("../assets/team/*.webp", {
  eager: true,
  query: "?url",
  import: "default",
});

function urlFor(file: string) {
  const url = urls[`../assets/team/${file}`];
  if (!url) throw new Error(`Missing processed photo ${file}. Run npm run images.`);
  return url;
}

/** Every portrait is shown at the same size: 11rem (176 px at default text size), 4:5. */
const frame = "block aspect-[4/5] w-44 rounded";

export function Portrait({
  photo,
  name,
  alt,
}: {
  photo?: string | undefined;
  name: string;
  alt: string;
}) {
  const sources = photo ? photos[photo] : undefined;
  const largest = sources?.at(-1);

  if (!sources || !largest) {
    const initials = name
      .split(/\s+/)
      .filter(Boolean)
      .map((part) => part[0])
      .filter((_, index, all) => index === 0 || index === all.length - 1)
      .join("")
      .toUpperCase();
    return (
      <div
        aria-hidden="true"
        className={`${frame} flex items-center justify-center border-2 border-control bg-surface text-5xl font-bold text-muted`}
      >
        {initials}
      </div>
    );
  }

  return (
    <img
      src={urlFor(largest.file)}
      srcSet={sources.map((s) => `${urlFor(s.file)} ${s.width}w`).join(", ")}
      sizes="11rem"
      width={largest.width}
      height={largest.height}
      alt={alt}
      loading="lazy"
      decoding="async"
      className={`${frame} h-auto bg-surface object-cover`}
    />
  );
}
