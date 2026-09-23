import React, { useState, useEffect } from 'react';
import { Network, Compass, FileText, Sparkles, AlertTriangle, Archive, Info, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';
import { api } from '../services/api';
import { translations } from '../i18n/translations';

export default function KnowledgeGraphView({ branchId = 'karagattam', lang = 'en' }) {
  const [graphData, setGraphData] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [loading, setLoading] = useState(true);
  const [zoom, setZoom] = useState(1);
  const t = translations[lang];

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    api.getGraph(branchId)
      .then((data) => {
        if (mounted) {
          setGraphData(data);
          if (data.nodes.length > 0) {
            setSelectedNode(data.nodes[1] || data.nodes[0]);
          }
          setLoading(false);
        }
      })
      .catch((err) => {
        console.error('Failed to load graph:', err);
        if (mounted) setLoading(false);
      });

    return () => { mounted = false; };
  }, [branchId]);

  if (loading) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-12 text-center space-y-3">
        <div className="w-8 h-8 border-3 border-amber-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p className="text-xs text-slate-500 font-medium">Generating interactive cultural knowledge graph...</p>
      </div>
    );
  }

  if (!graphData || graphData.nodes.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-8 text-center text-sm text-slate-500">
        No graph relationships found for this branch.
      </div>
    );
  }

  // Node styles by type
  const getNodeColor = (type) => {
    switch (type) {
      case 'domain':
        return { fill: '#6B1D2F', stroke: '#FDE68A', text: '#FFFFFF', icon: Compass };
      case 'branch':
        return { fill: '#B85D19', stroke: '#FED7AA', text: '#FFFFFF', icon: Compass };
      case 'source':
        return { fill: '#1F3A52', stroke: '#BAE6FD', text: '#FFFFFF', icon: FileText };
      case 'element':
        return { fill: '#059669', stroke: '#A7F3D0', text: '#FFFFFF', icon: Sparkles };
      case 'gap':
        return { fill: '#DC2626', stroke: '#FECACA', text: '#FFFFFF', icon: AlertTriangle };
      case 'preserved':
        return { fill: '#0D9488', stroke: '#99F6E4', text: '#FFFFFF', icon: Archive };
      default:
        return { fill: '#475569', stroke: '#CBD5E1', text: '#FFFFFF', icon: Network };
    }
  };

  // Organize nodes into layers for clear hierarchical DAG layout
  const layers = {
    domain: [],
    branch: [],
    source: [],
    element: [],
    gap: [],
    preserved: []
  };

  graphData.nodes.forEach((n) => {
    if (layers[n.type]) {
      layers[n.type].push(n);
    } else {
      layers.element.push(n);
    }
  });

  const layerOrder = ['domain', 'branch', 'source', 'element', 'gap', 'preserved'];
  const svgWidth = 840;
  const svgHeight = 560;

  // Calculate coordinates
  const nodePositions = {};
  const activeLayers = layerOrder.filter((l) => layers[l].length > 0);
  const colWidth = svgWidth / (activeLayers.length + 1);

  activeLayers.forEach((layerKey, colIdx) => {
    const layerNodes = layers[layerKey];
    const x = colWidth * (colIdx + 1);
    const rowHeight = svgHeight / (layerNodes.length + 1);

    layerNodes.forEach((node, rowIdx) => {
      const y = rowHeight * (rowIdx + 1);
      nodePositions[node.id] = { x, y };
    });
  });

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs">
      {/* Header Controls */}
      <div className="px-6 py-4 border-b border-slate-200 bg-slate-50/70 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="text-base font-bold text-slate-900 font-serif-title flex items-center space-x-2">
            <Network className="w-4 h-4 text-[#6B1D2F]" />
            <span>{lang === 'ta' ? 'அறிவு உறவு வரைபடம்' : 'Interactive Cultural Knowledge Graph'}</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Domain &rarr; Branch &rarr; Sources &rarr; Knowledge Elements &rarr; Potential Gaps &rarr; Preserved Knowledge
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setZoom((z) => Math.min(1.6, z + 0.15))}
            className="p-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-600"
            title="Zoom In"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={() => setZoom((z) => Math.max(0.6, z - 0.15))}
            className="p-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-600"
            title="Zoom Out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <button
            onClick={() => setZoom(1)}
            className="p-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-600"
            title="Reset Zoom"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4">
        {/* Graph Canvas */}
        <div className="lg:col-span-3 bg-slate-50/30 overflow-auto p-4 flex items-center justify-center min-h-[460px]">
          <svg
            width={svgWidth * zoom}
            height={svgHeight * zoom}
            viewBox={`0 0 ${svgWidth} ${svgHeight}`}
            className="transition-transform duration-200"
          >
            <defs>
              <marker
                id="arrowhead"
                markerWidth="8"
                markerHeight="6"
                refX="20"
                refY="3"
                orient="auto"
              >
                <polygon points="0 0, 8 3, 0 6" fill="#94A3B8" />
              </marker>
            </defs>

            {/* Edges */}
            {graphData.edges.map((edge) => {
              const from = nodePositions[edge.source];
              const to = nodePositions[edge.target];
              if (!from || !to) return null;

              return (
                <line
                  key={edge.id}
                  x1={from.x}
                  y1={from.y}
                  x2={to.x}
                  y2={to.y}
                  stroke="#CBD5E1"
                  strokeWidth="1.5"
                  strokeDasharray={edge.label === 'detected_gap' ? '4 2' : 'none'}
                  markerEnd="url(#arrowhead)"
                />
              );
            })}

            {/* Nodes */}
            {graphData.nodes.map((node) => {
              const pos = nodePositions[node.id];
              if (!pos) return null;
              const style = getNodeColor(node.type);
              const isSelected = selectedNode?.id === node.id;

              return (
                <g
                  key={node.id}
                  transform={`translate(${pos.x}, ${pos.y})`}
                  onClick={() => setSelectedNode(node)}
                  className="cursor-pointer transition-transform hover:scale-110"
                >
                  <circle
                    r={isSelected ? 20 : 16}
                    fill={style.fill}
                    stroke={isSelected ? '#F59E0B' : style.stroke}
                    strokeWidth={isSelected ? '3' : '2'}
                    className="drop-shadow-xs"
                  />
                  <text
                    y={28}
                    textAnchor="middle"
                    fontSize="9"
                    fontWeight={isSelected ? 'bold' : 'normal'}
                    fill="#1E293B"
                    className="select-none pointer-events-none"
                  >
                    {node.label.length > 18 ? node.label.slice(0, 16) + '..' : node.label}
                  </text>
                  <circle r={3} fill="#FFFFFF" cy={0} cx={0} />
                </g>
              );
            })}
          </svg>
        </div>

        {/* Selected Node Inspector */}
        <div className="border-t lg:border-t-0 lg:border-l border-slate-200 p-5 bg-white space-y-4">
          <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-slate-400">
            <Info className="w-4 h-4 text-slate-500" />
            <span>Node Inspector</span>
          </div>

          {selectedNode ? (
            <div className="space-y-3">
              <div>
                <span
                  className="inline-block px-2 py-0.5 rounded text-2xs font-extrabold uppercase tracking-wider"
                  style={{
                    backgroundColor: getNodeColor(selectedNode.type).fill + '20',
                    color: getNodeColor(selectedNode.type).fill
                  }}
                >
                  {selectedNode.type}
                </span>
                <h4 className="mt-1 text-base font-bold text-slate-900 font-serif-title">
                  {selectedNode.label}
                </h4>
              </div>

              <div className="text-xs text-slate-600 space-y-1.5 bg-slate-50 p-3 rounded-lg border border-slate-100">
                {selectedNode.data &&
                  Object.entries(selectedNode.data).map(([k, v]) => (
                    <div key={k} className="flex justify-between border-b border-slate-200/50 pb-1">
                      <span className="capitalize font-medium text-slate-500">{k.replace('_', ' ')}:</span>
                      <span className="font-semibold text-slate-800 truncate max-w-[140px]">{String(v)}</span>
                    </div>
                  ))}
              </div>

              <p className="text-2xs text-slate-400 leading-relaxed italic">
                *Click any linked node on canvas to explore provenance ancestry.
              </p>
            </div>
          ) : (
            <p className="text-xs text-slate-400 italic">Select a node to inspect relationships.</p>
          )}
        </div>
      </div>
    </div>
  );
}
