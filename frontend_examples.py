"""
Example Frontend Integration Code
Demonstrates how to call the KATA Testing API from React/Next.js/Vue/Angular
"""

# ============================================================================
# TypeScript/React Example
# ============================================================================

typescript_example = """
// api/degradedResponses.ts
// TypeScript interfaces for type safety

export interface DegradedResponse {
  "Serial Number": string;
  "Prompt": string;
  "Old Response (Benchmark)": string;
  "New Response": string;
  "Old Sources": string;
  "New Sources": string;
  "Benchmark Quality": string;
  "Degradation Reason": string;
  "Severity": "HIGH" | "MEDIUM";
}

export interface SheetData {
  sheet_name: string;
  row_count: number;
  data: DegradedResponse[];
}

export interface AllDegradedResponsesApiResponse {
  total_sheets: number;
  total_issues: number;
  last_updated: string;
  sheets: SheetData[];
}

export interface SingleSheetApiResponse {
  sheet_name: string;
  total_issues: number;
  last_updated: string;
  data: DegradedResponse[];
}

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Fetch all degraded responses from all sheets
 */
export async function getAllDegradedResponses(): Promise<AllDegradedResponsesApiResponse> {
  const response = await fetch(`${API_BASE_URL}/api/degraded-responses`);
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Fetch degraded responses for a specific sheet
 * @param sheetName - One of: "PSP Mentor", "VSM Mentor", "TPI Mentor", "Search/Chat"
 */
export async function getDegradedResponsesBySheet(
  sheetName: string
): Promise<SingleSheetApiResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/degraded-responses/${encodeURIComponent(sheetName)}`
  );
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Force refresh the API cache
 */
export async function refreshCache(): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/refresh`, {
    method: 'POST',
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
}

/**
 * Check API health status
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  
  return response.json();
}
"""

# ============================================================================
# React Component Example
# ============================================================================

react_component_example = """
// components/DegradedResponsesTable.tsx
import { useState, useEffect } from 'react';
import { getAllDegradedResponses, AllDegradedResponsesApiResponse } from '../api/degradedResponses';

export default function DegradedResponsesTable() {
  const [data, setData] = useState<AllDegradedResponsesApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSheet, setSelectedSheet] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const result = await getAllDegradedResponses();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 m-4">
        <h3 className="text-red-800 font-semibold">Error Loading Data</h3>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!data || data.total_issues === 0) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 m-4">
        <h3 className="text-green-800 font-semibold">✅ No Issues Found</h3>
        <p className="text-green-600">All API responses are performing well!</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      {/* Summary Header */}
      <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
        <h1 className="text-3xl font-bold mb-2">Degraded Responses Report</h1>
        <div className="grid grid-cols-3 gap-4 mt-4">
          <div className="bg-blue-50 p-4 rounded">
            <p className="text-sm text-gray-600">Total Issues</p>
            <p className="text-2xl font-bold text-blue-600">{data.total_issues}</p>
          </div>
          <div className="bg-purple-50 p-4 rounded">
            <p className="text-sm text-gray-600">Sheets Affected</p>
            <p className="text-2xl font-bold text-purple-600">{data.total_sheets}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded">
            <p className="text-sm text-gray-600">Last Updated</p>
            <p className="text-sm font-semibold text-gray-700">
              {new Date(data.last_updated).toLocaleString()}
            </p>
          </div>
        </div>
      </div>

      {/* Sheet Tabs */}
      <div className="flex gap-2 mb-4 overflow-x-auto">
        <button
          onClick={() => setSelectedSheet(null)}
          className={`px-4 py-2 rounded whitespace-nowrap ${
            selectedSheet === null
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All Sheets
        </button>
        {data.sheets.map((sheet) => (
          <button
            key={sheet.sheet_name}
            onClick={() => setSelectedSheet(sheet.sheet_name)}
            className={`px-4 py-2 rounded whitespace-nowrap ${
              selectedSheet === sheet.sheet_name
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {sheet.sheet_name} ({sheet.row_count})
          </button>
        ))}
      </div>

      {/* Data Tables */}
      {data.sheets
        .filter((sheet) => selectedSheet === null || sheet.sheet_name === selectedSheet)
        .map((sheet) => (
          <div key={sheet.sheet_name} className="bg-white shadow-lg rounded-lg p-6 mb-6">
            <h2 className="text-2xl font-bold mb-4">{sheet.sheet_name}</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Serial
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Prompt
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Reason
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Severity
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {sheet.data.map((row, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-4 py-3 whitespace-nowrap text-sm">
                        {row['Serial Number']}
                      </td>
                      <td className="px-4 py-3 text-sm max-w-md">
                        <div className="line-clamp-2">{row['Prompt']}</div>
                      </td>
                      <td className="px-4 py-3 text-sm max-w-md">
                        <div className="line-clamp-2">{row['Degradation Reason']}</div>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span
                          className={`px-2 py-1 text-xs font-semibold rounded-full $
                            row.Severity === 'HIGH'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}
                        >
                          {row.Severity}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
    </div>
  );
}
"""

# ============================================================================
# Vue.js Example
# ============================================================================

vue_example = """
<!-- components/DegradedResponsesTable.vue -->
<template>
  <div class="container mx-auto p-4">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center p-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <h3 class="text-red-800 font-semibold">Error Loading Data</h3>
      <p class="text-red-600">{{ error }}</p>
    </div>

    <!-- Data Display -->
    <div v-else-if="data">
      <!-- Summary -->
      <div class="bg-white shadow-lg rounded-lg p-6 mb-6">
        <h1 class="text-3xl font-bold mb-4">Degraded Responses Report</h1>
        <div class="grid grid-cols-3 gap-4">
          <div class="bg-blue-50 p-4 rounded">
            <p class="text-sm text-gray-600">Total Issues</p>
            <p class="text-2xl font-bold text-blue-600">{{ data.total_issues }}</p>
          </div>
          <div class="bg-purple-50 p-4 rounded">
            <p class="text-sm text-gray-600">Sheets Affected</p>
            <p class="text-2xl font-bold text-purple-600">{{ data.total_sheets }}</p>
          </div>
          <div class="bg-gray-50 p-4 rounded">
            <p class="text-sm text-gray-600">Last Updated</p>
            <p class="text-sm font-semibold text-gray-700">
              {{ formatDate(data.last_updated) }}
            </p>
          </div>
        </div>
      </div>

      <!-- Tables -->
      <div v-for="sheet in data.sheets" :key="sheet.sheet_name" 
           class="bg-white shadow-lg rounded-lg p-6 mb-6">
        <h2 class="text-2xl font-bold mb-4">{{ sheet.sheet_name }}</h2>
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Serial
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Prompt
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Severity
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(row, idx) in sheet.data" :key="idx" class="hover:bg-gray-50">
              <td class="px-4 py-3 whitespace-nowrap text-sm">
                {{ row['Serial Number'] }}
              </td>
              <td class="px-4 py-3 text-sm">{{ row['Prompt'] }}</td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span :class="getSeverityClass(row.Severity)">
                  {{ row.Severity }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const data = ref(null);
const loading = ref(true);
const error = ref(null);

async function fetchData() {
  try {
    loading.value = true;
    const response = await fetch(`${API_BASE_URL}/api/degraded-responses`);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    data.value = await response.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleString();
}

function getSeverityClass(severity: string) {
  return severity === 'HIGH'
    ? 'px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800'
    : 'px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800';
}

onMounted(() => {
  fetchData();
});
</script>
"""

# ============================================================================
# Plain JavaScript (Vanilla) Example
# ============================================================================

vanilla_js_example = """
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Degraded Responses Report</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
  <div id="app" class="container mx-auto p-4"></div>

  <script>
    const API_BASE_URL = 'http://localhost:8000';

    async function fetchDegradedResponses() {
      const appDiv = document.getElementById('app');
      appDiv.innerHTML = '<div class="text-center p-8">Loading...</div>';

      try {
        const response = await fetch(`${API_BASE_URL}/api/degraded-responses`);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        renderData(data);
      } catch (error) {
        appDiv.innerHTML = `
          <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <h3 class="text-red-800 font-semibold">Error Loading Data</h3>
            <p class="text-red-600">${error.message}</p>
          </div>
        `;
      }
    }

    function renderData(data) {
      const appDiv = document.getElementById('app');
      
      let html = `
        <div class="bg-white shadow-lg rounded-lg p-6 mb-6">
          <h1 class="text-3xl font-bold mb-4">Degraded Responses Report</h1>
          <div class="grid grid-cols-3 gap-4">
            <div class="bg-blue-50 p-4 rounded">
              <p class="text-sm text-gray-600">Total Issues</p>
              <p class="text-2xl font-bold text-blue-600">${data.total_issues}</p>
            </div>
            <div class="bg-purple-50 p-4 rounded">
              <p class="text-sm text-gray-600">Sheets Affected</p>
              <p class="text-2xl font-bold text-purple-600">${data.total_sheets}</p>
            </div>
            <div class="bg-gray-50 p-4 rounded">
              <p class="text-sm text-gray-600">Last Updated</p>
              <p class="text-sm font-semibold text-gray-700">
                ${new Date(data.last_updated).toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      `;

      data.sheets.forEach(sheet => {
        html += `
          <div class="bg-white shadow-lg rounded-lg p-6 mb-6">
            <h2 class="text-2xl font-bold mb-4">${sheet.sheet_name}</h2>
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Serial</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Prompt</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Severity</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
        `;

        sheet.data.forEach(row => {
          const severityClass = row.Severity === 'HIGH'
            ? 'bg-red-100 text-red-800'
            : 'bg-yellow-100 text-yellow-800';

          html += `
            <tr class="hover:bg-gray-50">
              <td class="px-4 py-3 whitespace-nowrap text-sm">${row['Serial Number']}</td>
              <td class="px-4 py-3 text-sm">${row['Prompt']}</td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span class="px-2 py-1 text-xs font-semibold rounded-full ${severityClass}">
                  ${row.Severity}
                </span>
              </td>
            </tr>
          `;
        });

        html += `
              </tbody>
            </table>
          </div>
        `;
      });

      appDiv.innerHTML = html;
    }

    // Fetch data on page load
    fetchDegradedResponses();

    // Auto-refresh every 5 minutes
    setInterval(fetchDegradedResponses, 5 * 60 * 1000);
  </script>
</body>
</html>
"""

# Print examples
if __name__ == "__main__":
    print("="*70)
    print("Frontend Integration Examples")
    print("="*70)
    
    print("\n" + "="*70)
    print("1. TypeScript/React API Client")
    print("="*70)
    print(typescript_example)
    
    print("\n" + "="*70)
    print("2. React Component")
    print("="*70)
    print(react_component_example)
    
    print("\n" + "="*70)
    print("3. Vue.js Component")
    print("="*70)
    print(vue_example)
    
    print("\n" + "="*70)
    print("4. Vanilla JavaScript")
    print("="*70)
    print(vanilla_js_example)
