// Main JavaScript functionality
document.addEventListener("DOMContentLoaded", function () {
  // Initialize Dark Mode
  initDarkMode();

  // Initialize Navigation
  initNavigation();

  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]'),
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Form validation
  const forms = document.querySelectorAll(".needs-validation");
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add("was-validated");
      },
      false,
    );
  });

  // Prediction form handling
  const predictionForm = document.getElementById("prediction-form");
  if (predictionForm) {
    predictionForm.addEventListener("submit", function (e) {
      const submitBtn = this.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;

      submitBtn.innerHTML = '<span class="spinner"></span> Predicting...';
      submitBtn.disabled = true;

      // Re-enable button after 3 seconds (in case of error)
      setTimeout(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
      }, 3000);
    });
  }

  // Auto-hide alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.opacity = "0";
      setTimeout(() => {
        alert.remove();
      }, 300);
    }, 5000);
  });

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Dashboard chart initialization (if Plotly is available)
  if (typeof Plotly !== "undefined") {
    initializeDashboardCharts();
  }
});

// Navigation Management
function initNavigation() {
  // Highlight active page
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-feature');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    
    // Check if current path matches the link
    if (href === currentPath || 
        (currentPath === '/' && href.includes('dashboard')) ||
        (currentPath.includes('predict') && href.includes('predict')) ||
        (currentPath.includes('history') && href.includes('history')) ||
        (currentPath.includes('bulk') && href.includes('bulk')) ||
        (currentPath.includes('admin') && href.includes('admin'))) {
      link.classList.add('active');
    }
  });
}

// Dark Mode Management
function initDarkMode() {
  // Check for saved preference or system preference
  const savedMode = localStorage.getItem("darkMode");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const isDarkMode = savedMode ? JSON.parse(savedMode) : prefersDark;

  if (isDarkMode) {
    enableDarkMode();
  }

  // Listen for theme toggle button
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", toggleDarkMode);
    updateThemeToggleIcon();
  }
}

function toggleDarkMode() {
  const body = document.body;
  const isDarkMode = body.classList.contains("dark-mode");

  if (isDarkMode) {
    disableDarkMode();
  } else {
    enableDarkMode();
  }
}

function enableDarkMode() {
  document.body.classList.add("dark-mode");
  localStorage.setItem("darkMode", "true");
  updateThemeToggleIcon();
  
  // Force all text to be white in dark mode
  const style = document.createElement('style');
  style.innerHTML = `
    body.dark-mode, body.dark-mode * {
      color: #ffffff !important;
    }
    body.dark-mode .btn {
      color: white !important;
    }
    body.dark-mode .badge-danger {
      color: white !important;
      background-color: #dc2626 !important;
    }
    body.dark-mode .badge-success {
      color: white !important;
      background-color: #10b981 !important;
    }
    body.dark-mode .table {
      background-color: #1e293b !important;
    }
    body.dark-mode .card {
      background-color: #1e293b !important;
    }
  `;
  document.head.appendChild(style);
  
  // Refresh charts if they exist
  setTimeout(() => {
    if (typeof refreshDashboardCharts === 'function') {
      refreshDashboardCharts();
    }
    if (typeof initializeDashboardCharts === 'function') {
      initializeDashboardCharts();
    }
  }, 100);
}

function disableDarkMode() {
  document.body.classList.remove("dark-mode");
  localStorage.setItem("darkMode", "false");
  updateThemeToggleIcon();
  
  // Refresh charts if they exist
  setTimeout(() => {
    if (typeof refreshDashboardCharts === 'function') {
      refreshDashboardCharts();
    }
    if (typeof initializeDashboardCharts === 'function') {
      initializeDashboardCharts();
    }
  }, 100);
}

function updateThemeToggleIcon() {
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    const isDarkMode = document.body.classList.contains("dark-mode");
    const icon = themeToggle.querySelector("i");

    if (isDarkMode) {
      icon.classList.remove("fa-moon");
      icon.classList.add("fa-sun");
      themeToggle.setAttribute("title", "Light Mode");
    } else {
      icon.classList.remove("fa-sun");
      icon.classList.add("fa-moon");
      themeToggle.setAttribute("title", "Dark Mode");
    }
  }
}

// Dashboard charts
function initializeDashboardCharts() {
  // Prediction distribution chart
  const predictionDistChart = document.getElementById(
    "prediction-distribution",
  );
  if (predictionDistChart) {
    fetch("/api/prediction-stats")
      .then((response) => response.json())
      .then((data) => {
        const trace = {
          x: ["No Churn", "Churn"],
          y: [data.no_churn, data.churn],
          type: "bar",
          marker: {
            color: ["#10b981", "#ef4444"],
          },
        };

        const layout = getPlotlyLayout("Prediction Distribution", "Prediction", "Count");

        Plotly.newPlot("prediction-distribution", [trace], layout, {
          responsive: true,
        });
      })
      .catch((error) =>
        console.error("Error loading prediction stats:", error),
      );
  }

  // Monthly predictions trend
  const monthlyTrendChart = document.getElementById("monthly-trend");
  if (monthlyTrendChart) {
    fetch("/api/monthly-trend")
      .then((response) => response.json())
      .then((data) => {
        const trace = {
          x: data.months,
          y: data.counts,
          type: "scatter",
          mode: "lines+markers",
          line: { color: "#667eea", width: 3 },
          marker: { color: "#667eea", size: 8 },
        };

        const layout = getPlotlyLayout("Monthly Predictions Trend", "Month", "Number of Predictions");

        Plotly.newPlot("monthly-trend", [trace], layout, { responsive: true });
      })
      .catch((error) => console.error("Error loading monthly trend:", error));
  }
}

// Get Plotly layout with proper dark mode support
function getPlotlyLayout(title, xTitle, yTitle) {
  const isDarkMode = document.body.classList.contains("dark-mode");
  
  return {
    title: {
      text: title,
      font: {
        color: isDarkMode ? "#ffffff" : "#1e293b",
        size: 16
      }
    },
    xaxis: { 
      title: {
        text: xTitle,
        font: {
          color: isDarkMode ? "#ffffff" : "#1e293b"
        }
      },
      tickfont: {
        color: isDarkMode ? "#ffffff" : "#1e293b"
      },
      gridcolor: isDarkMode ? "#475569" : "#e2e8f0"
    },
    yaxis: { 
      title: {
        text: yTitle,
        font: {
          color: isDarkMode ? "#ffffff" : "#1e293b"
        }
      },
      tickfont: {
        color: isDarkMode ? "#ffffff" : "#1e293b"
      },
      gridcolor: isDarkMode ? "#475569" : "#e2e8f0"
    },
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
    font: {
      color: isDarkMode ? "#ffffff" : "#1e293b"
    }
  };
}

// Utility functions
function showAlert(message, type = "info") {
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
  alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  const container = document.querySelector(".main-container");
  if (container) {
    container.insertBefore(alertDiv, container.firstChild);

    // Auto-hide after 5 seconds
    setTimeout(() => {
      alertDiv.style.opacity = "0";
      setTimeout(() => {
        alertDiv.remove();
      }, 300);
    }, 5000);
  }
}

function formatCurrency(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
