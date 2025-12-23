import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip
);

function formatDateByRange(dateStr, range) {
  const date = new Date(dateStr);

  if (["1w", "1mo"].includes(range)) {
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    });
  }

  if (["6mo", "1y"].includes(range)) {
    return date.toLocaleDateString("en-US", {
      month: "short",
    });
  }

  // 3y, 5y, all
  return date.getFullYear().toString();
}

export default function PriceChart({ data, range }) {
  if (!data || data.length === 0) {
    return <p>No chart data</p>;
  }

  const labels = data.map(d => d.date);
  const prices = data.map(d => Number(d.close));

  const chartData = {
    labels,
    datasets: [
      {
        data: prices,
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59,130,246,0.1)",
        tension: 0.25,
        pointRadius: 0,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          title: (ctx) => {
            const date = ctx[0].label;
            return new Date(date).toLocaleDateString("en-US", {
              year: "numeric",
              month: "short",
              day: "numeric",
            });
          },
          label: (ctx) => `₹ ${ctx.parsed.y.toFixed(2)}`,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#9ca3af",
          maxTicksLimit: 6,
          callback: function (value) {
            const dateStr = this.getLabelForValue(value);
            return formatDateByRange(dateStr, range);
          },
        },
        grid: {
          display: false,
        },
      },
      y: {
        ticks: {
          color: "#9ca3af",
        },
        grid: {
          color: "rgba(255,255,255,0.05)",
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
}
