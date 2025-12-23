import { RANGE_TO_DAYS } from "../constants/ranges";

export default function RangeSelector({ active, onChange }) {
  return (
    <div className="range-selector">
      {Object.keys(RANGE_TO_DAYS).map(range => (
        <button
          key={range}
          className={active === range ? "active" : ""}
          onClick={() => onChange(range)}
        >
          {range}
        </button>
      ))}
    </div>
  );
}
