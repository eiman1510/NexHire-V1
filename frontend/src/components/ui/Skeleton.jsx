export default function Skeleton({ count = 3, className = "" }) {
  return (
    <>
      {Array.from({ length: count }).map((_, index) => (
        <div className={`skeleton ${className}`} key={index}>
          <span />
          <span />
          <span />
        </div>
      ))}
    </>
  );
}
