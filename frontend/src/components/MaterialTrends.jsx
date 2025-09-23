import React, { useEffect, useState } from "react";
import { collection, getDocs } from "firebase/firestore";
import { db } from "../firebase";

function Sparkline({ data, width = 100, height = 30 }) {
    if (!Array.isArray(data) || data.length === 0) return null;

    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min || 1;

    const points = data.map((d, i) => {
        const x = (i / (data.length - 1)) * width;
        const y = height - ((d - min) / range) * height;
        return `${x},${y}`;
    });

    return (
        <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
            <polyline
                fill="none"
                stroke="#6366f1"
                strokeWidth="2"
                points={points.join(" ")}
            />
        </svg>
    );
}

// === CATEGORY MAP ===
const categoryMap = {
    "Overhead Ecnomic Indicators": [
        "Consumer Price Index (CPI-U)",
        "Producer Price Index (PPI For Final Demand",
        "Unemployment Rate",
        "Labor Force Participation Rate",
        "Construction Employment"
    ],
    "Construction Indexes and Inputs": [
        "Final Demand Construction",
        "Inputs to Construction Industries",
        "Inputs to Construction Industries, Energy",
        "Inputs to Construction Industries, Goods",
        "Inputs to Construction Industries, Goods Less Foods",
        "Inputs to Construction Industries, Services",
        "Construction (Partial)"
    ],
    "Contractors/Services": [
        "Electrical Contractors",
        "Plumbing Contractors",
        "Roofing Contractors",
        "Concrete Contractors",
        "Engineering Services",
        "Architectural Services"
    ],
    "Metals": [
        "Copper and Brass Mill Shapes",
        "Copper Base Scrap",
        "Steel Mill Products",
        "Fabricated Structural Metal",
        "Fabricated Structural Metal Bar Joists and Rebar",
        "Fabricated Structural Metal for Bridges",
        "Fabricated Structural Metal for Non-Industrial Buildings",
        "Fabricated Steel Plate",
        "Iron and Steel Scrap",
        "Stainless and Alloy Steel Scrap",
        "Prefabricated Metal Buildings",
        "Ornamental and Architectural Metal Work",
        "Sheet Metal Products",
        "Steel Pipe and Tube",
        "Aluminum Mill Shapes"
    ],
    "Concrete": [
        "Ready Mixed Concrete",
        "Concrete Pipe",
        "Concrete Products",
        "Precast Concrete Products",
        "Prestressed Concrete Products",
        "Concrete Block and Brick",
        "Brick and Structural Clay Tile",
        "Cement",
        "Gypsum Building MAterials"
    ],
    "Asphalts": [
        "#2 Diesel Fuel",
        "Asphalt (At Refinery)",
        "Asphalt Felts and Coatings",
        "Prepared Asphalt and Tar Rooging and Siding Products",
        "Paving Mixtures"
    ],
    "General": [
        "Plastic Construction Products",
        "Lumber and Plywood",
        "Insulation Materials",
        "Truck Transportation of Freight",
        "Truck and Bus (Inc Off Highway) Pneumatic Tires",
        "Const, Mining & Forestry Machine and Equipment. Rental and Leasing",
        "Construction MAchinery and Equipment"
    ],
    "Construction Types": [
        "Architectural Coatings",
        "Flatt Glass",
        "Construction and Sand/Gravel/Crushed Stone",
        "Construction for Government",
        "New Nonresedential Construction",
        "New Nonresidential Building Construction",
        "New Warehouse Building Construction",
        "New School Building Construction",
        "New Office Building Construction",
        "New Industrial Building Construction",
        "New Health Care Building Construction",
        "Maint & Repair of Nonres Buildings (Partial)",
        "Construction for Private Capital Investment",
        "Construction for Government",
        "New Residential Construction",
        "Multifamily",
        "New Nonresedential Construction",
        "Commercial Structures",
        "Healthcare Structures",
        "Industrial Structures",
        "Other Non Residential",
        "Highways and Streets",
        "Power and Communications Structiors",
        "Education and Vocational Structures",
        "Other Misc. Non Residential Construction",
        "Mainenance and Repair Construction",
        "Residential Maintenance and Repair",
        "Nonresidential Maintenance and Repair"
    ]
};

function getCategory(name) {
    const cleaned = name?.trim();
    for (const [category, names] of Object.entries(categoryMap)) {
        if (names.includes(cleaned)) return category;
    }
    console.warn("🚨 Unmatched series name:", cleaned);
    return "Uncategorized";
}



export default function MaterialTrends() {
    const [materials, setMaterials] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchData() {
            try {
                const snapshot = await getDocs(collection(db, "materialTrends"));

                const rawData = snapshot.docs.map((doc) => {
                    const raw = doc.data();
                    const observations = raw.observations || [];
                    const sorted = observations.sort((a, b) => a.date.localeCompare(b.date));
                    const last = sorted[sorted.length - 1] || {};
                    const recentValues = sorted.slice(-36).map((obs) => obs.value);

                    return {
                        id: doc.id,
                        name: raw.series_name,
                        mom: last.mom_growth,
                        yoy: last.yoy_growth,
                        trend: recentValues,
                        latestDate: last.date, // Add the latest date
                        category: getCategory(raw.series_name),
                    };
                });

                // ❄️ Purge blank entries
                const cleaned = rawData.filter((d) => {
                    const isValidName = d.name && d.name !== "—";
                    const hasData =
                        d.mom !== undefined ||
                        d.yoy !== undefined ||
                        (Array.isArray(d.trend) && d.trend.length > 0);
                    return isValidName && hasData;
                });

                setMaterials(cleaned);
            } catch (err) {
                console.error("🔥 Firestore fetch failed:", err);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, []);

return (
    <div
        style={{ 
            backgroundColor: "#BE6428", 
            fontFamily: "josefin-sans, sans-serif",
            minHeight: "100vh",
            padding: "1rem"
        }}
    >
        {/* Banner header */}
        <div style={{
            background: 'linear-gradient(90deg, #1f2937 0%, #334155 100%)',
            color: 'white',
            borderRadius: '16px',
            padding: '20px 16px',
            boxShadow: '0 12px 24px rgba(0,0,0,0.15)',
            marginBottom: '12px'
        }}>
            <h1 style={{ 
                fontSize: '3.5rem', 
                fontWeight: '900', 
                margin: 0,
                textAlign: 'center',
                letterSpacing: '0.04em'
            }}>
                WHAT'S IT COST
            </h1>
            <div style={{ textAlign: 'center', marginTop: '6px' }}>
                <p style={{
                    color: '#e5e7eb',
                    fontWeight: 700,
                    fontSize: '1.25rem',
                    margin: 0
                }}>
                    Your Source For The Latest In BLS Pricing Data
                </p>
            </div>
            {/* Latest BLS Month Display */}
            {!loading && materials.length > 0 && (
                <div style={{ textAlign: 'center', marginTop: '8px' }}>
                    <p style={{ 
                        color: '#e2e8f0', 
                        fontWeight: 600, 
                        fontSize: '1.25rem',
                        margin: 0
                    }}>
                        Data Current To {(() => {
                        // Find the latest month from all materials
                        let latestMonth = null;
                        materials.forEach(material => {
                            if (material.latestDate) {
                                // Parse YYYY-MM format (e.g., "2025-07")
                                const [year, month] = material.latestDate.split('-');
                                if (year && month) {
                                    const monthDate = new Date(parseInt(year), parseInt(month) - 1, 1);
                                    if (!latestMonth || monthDate > latestMonth) {
                                        latestMonth = monthDate;
                                    }
                                }
                            }
                        });
                        
                        if (latestMonth) {
                            return latestMonth.toLocaleDateString('en-US', { 
                                year: 'numeric', 
                                month: 'long' 
                            });
                        }
                        return 'N/A';
                    })()}
                    </p>
                </div>
            )}
        </div>

        {loading ? (
            <p style={{ 
                color: '#6b7280', 
                fontSize: '1.125rem', 
                textAlign: 'center' 
            }}>
                Loading data...
            </p>
        ) : materials.length === 0 ? (
            <p style={{ 
                color: '#dc2626', 
                fontSize: '1.125rem', 
                textAlign: 'center' 
            }}>
                No data found. Check Firestore or field names.
            </p>
        ) : (
            <div id="gridStart" style={{
                borderRadius: '0.75rem',
                boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                border: '1px solid #d1d5db',
                backgroundColor: 'white'
            }}>
                {Object.entries(
                    materials.reduce((acc, mat) => {
                        acc[mat.category] = acc[mat.category] || [];
                        acc[mat.category].push(mat);
                        return acc;
                    }, {})
                ).sort(([a], [b]) => {
                    const desiredOrder = [
                        "Overhead Ecnomic Indicators",
                        "Construction Indexes and Inputs"
                    ];
                    const indexA = desiredOrder.indexOf(a);
                    const indexB = desiredOrder.indexOf(b);
                    if (indexA === -1 && indexB === -1) return a.localeCompare(b);
                    if (indexA === -1) return 1;
                    if (indexB === -1) return -1;
                    return indexA - indexB;
                }).map(([category, group]) => (

                    <div key={category} style={{ position: "relative" }}>
                        <div
                            style={{
                                position: "sticky",
                                top: "0",
                                zIndex: 50,
                                backgroundColor: "#4DAAf8",
                                padding: "10px 0",
                                borderBottom: "2px solid #e2e8f0",
                                color: "white",
                                fontSize: "1.125rem",
                                fontWeight: "bold",
                                letterSpacing: "0.025em",
                                textAlign: "center",
                                boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
                            }}
                        >
                            {category}
                        </div>

                        <table className="w-full table-auto border-collapse text-sm sm:text-base">
                            <colgroup>
                                <col style={{ width: "40%" }} />
                                <col style={{ width: "20%" }} />
                                <col style={{ width: "20%" }} />
                                <col style={{ width: "20%" }} />
                            </colgroup>
                            <thead>
                                <tr>
                                    {["Material", "Month over Month", "Year over Year", "36-Month Trend"].map((label) => (
                                        <th
                                            key={label}
                                            className="text-xs sm:text-sm md:text-base"
                                            style={{
                                                position: "sticky",
                                                top: 44,
                                                zIndex: 40,
                                                color: "#f1f5f9",
                                                fontWeight: "700",
                                                backgroundColor: "#3886C8",
                                                letterSpacing: "1px",
                                                padding: "12px",
                                                textAlign: "center",
                                                borderRight: "1px solid #334155",
                                                textTransform: "uppercase",
                                                whiteSpace: "nowrap",
                                            }}
                                        >
                                            {label}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {group.map((mat) => (
                                    <tr key={mat.id}>
                                        <td
                                            className="text-xs sm:text-sm md:text-base"
                                            style={{
                                                fontWeight: "700",
                                                color: "#0f172a",
                                                backgroundColor: "#F6F6F6",
                                                padding: "12px",
                                                textAlign: "left",
                                                border: "1px solid #e2e8f0",
                                                textTransform: "uppercase",
                                            }}
                                        >
                                            {mat.name}
                                        </td>
                                        {[mat.mom, mat.yoy].map((val, idx) => (
                                            <td
                                                key={idx}
                                                className="text-xs sm:text-sm md:text-base"
                                                style={{
                                                    fontWeight: "600",
                                                    color: val < 0 ? "#dc2626" : "#16a34a",
                                                    textAlign: "center",
                                                    borderRight: "1px solid #e5e7eb",
                                                    padding: "12px",
                                                    backgroundColor: "#F6F6F6",
                                                }}
                                            >
                                                {val !== undefined
                                                    ? `${val.toFixed(2)}%`
                                                    : "—"}
                                            </td>
                                        ))}
                                        <td
                                            className="px-2 py-3 text-center border-r border-gray-200"
                                            style={{ backgroundColor: "#F6F6F6" }}
                                        >
                                            <Sparkline data={mat.trend} />
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ))}
            </div>
        )}
    </div>
);}