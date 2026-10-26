import React, { useState } from 'react';
import { 
  Cpu, 
  Coins, 
  Plus, 
  Radio, 
  Activity, 
  ShieldCheck, 
  Battery, 
  Wifi, 
  Thermometer, 
  Check, 
  ExternalLink,
  Zap,
  Building,
  Leaf
} from 'lucide-react';
import { IoTDevice, TokenizedAsset } from '../types';

interface AssetsIotViewProps {
  iotDevices: IoTDevice[];
  tokenizedAssets: TokenizedAsset[];
  onAddDevice: (device: { deviceId: string; deviceType: string; location: string }) => void;
  onAddAsset: (asset: { assetId: string; name: string; owner: string; tokenizedValue: number; category: TokenizedAsset['category'] }) => void;
}

export const AssetsIotView: React.FC<AssetsIotViewProps> = ({
  iotDevices,
  tokenizedAssets,
  onAddDevice,
  onAddAsset
}) => {
  // Device Data Alert state (matching dashboard.html '#device-data')
  const [activeDeviceData, setActiveDeviceData] = useState<{
    deviceId: string;
    metrics: IoTDevice['metrics'];
    deviceType: string;
    location: string;
  } | null>(null);

  // New device form modal
  const [isAddingDevice, setIsAddingDevice] = useState(false);
  const [newDeviceId, setNewDeviceId] = useState('');
  const [newDeviceType, setNewDeviceType] = useState('Environmental Weather Node');
  const [newDeviceLocation, setNewDeviceLocation] = useState('');

  // New asset form modal
  const [isAddingAsset, setIsAddingAsset] = useState(false);
  const [newAssetId, setNewAssetId] = useState('');
  const [newAssetName, setNewAssetName] = useState('');
  const [newAssetOwner, setNewAssetOwner] = useState('Pioneer Sovereign Trust');
  const [newAssetValue, setNewAssetValue] = useState('100000');
  const [newAssetCategory, setNewAssetCategory] = useState<TokenizedAsset['category']>('Renewable Energy');

  // Match dashboard.html `fetchDeviceData(deviceId)`
  const handleFetchDeviceData = (device: IoTDevice) => {
    setActiveDeviceData({
      deviceId: device.deviceId,
      metrics: {
        ...device.metrics,
        temperature: Number((device.metrics.temperature + (Math.random() * 0.8 - 0.4)).toFixed(1)),
        battery: Math.max(10, Math.min(100, Math.round(device.metrics.battery + (Math.random() * 2 - 1))))
      },
      deviceType: device.deviceType,
      location: device.location
    });
  };

  const handleDeviceSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newDeviceId.trim()) return;
    onAddDevice({
      deviceId: newDeviceId.trim(),
      deviceType: newDeviceType,
      location: newDeviceLocation.trim() || 'Global Distributed Station'
    });
    setNewDeviceId('');
    setNewDeviceLocation('');
    setIsAddingDevice(false);
  };

  const handleAssetSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAssetId.trim() || !newAssetName.trim()) return;
    onAddAsset({
      assetId: newAssetId.trim(),
      name: newAssetName.trim(),
      owner: newAssetOwner.trim(),
      tokenizedValue: parseFloat(newAssetValue) || 10000,
      category: newAssetCategory
    });
    setNewAssetId('');
    setNewAssetName('');
    setIsAddingAsset(false);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Overview Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Cpu className="w-5 h-5 text-blue-400" />
            Physical Layer: IoT Telemetry & Real-World Tokenized Assets
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Seamlessly bridge physical IoT sensors with decentralized tokenized assets on the Pi Network ledger.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setIsAddingDevice(true)}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white transition shadow-md shadow-blue-600/20"
          >
            <Plus className="w-4 h-4" />
            <span>Connect IoT Device</span>
          </button>
          <button
            onClick={() => setIsAddingAsset(true)}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-xs font-semibold text-white transition shadow-md shadow-purple-600/20"
          >
            <Plus className="w-4 h-4" />
            <span>Tokenize Asset</span>
          </button>
        </div>
      </div>

      {/* Real-Time Device Data Display (Matching original dashboard.html #device-data alert) */}
      {activeDeviceData && (
        <div className="p-5 rounded-2xl bg-blue-950/50 border border-blue-800/80 text-blue-100 shadow-xl relative animate-in fade-in">
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 rounded-xl bg-blue-500/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
                <Radio className="w-5 h-5 animate-pulse" />
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <h4 className="text-sm font-bold text-white">
                    Telemetry Stream: {activeDeviceData.deviceId}
                  </h4>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-900/60 text-blue-300 border border-blue-700/50">
                    {activeDeviceData.deviceType}
                  </span>
                </div>
                <p className="text-xs text-slate-300 mt-0.5">{activeDeviceData.location}</p>
              </div>
            </div>

            <button
              onClick={() => setActiveDeviceData(null)}
              className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-blue-900/50 hover:bg-blue-800/60 text-blue-200 transition"
            >
              Dismiss Stream
            </button>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 pt-4 border-t border-blue-900/50">
            <div className="bg-slate-950/60 p-3 rounded-xl border border-blue-900/30">
              <div className="text-[10px] text-slate-400 flex items-center gap-1 font-medium">
                <Battery className="w-3.5 h-3.5 text-emerald-400" /> Battery Level
              </div>
              <div className="text-sm font-mono font-bold text-white mt-1">
                {activeDeviceData.metrics.battery}%
              </div>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-xl border border-blue-900/30">
              <div className="text-[10px] text-slate-400 flex items-center gap-1 font-medium">
                <Wifi className="w-3.5 h-3.5 text-blue-400" /> Signal Quality
              </div>
              <div className="text-sm font-mono font-bold text-white mt-1">
                {activeDeviceData.metrics.signal} dBm (99%)
              </div>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-xl border border-blue-900/30">
              <div className="text-[10px] text-slate-400 flex items-center gap-1 font-medium">
                <Thermometer className="w-3.5 h-3.5 text-amber-400" /> Core Temp
              </div>
              <div className="text-sm font-mono font-bold text-white mt-1">
                {activeDeviceData.metrics.temperature} °C
              </div>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-xl border border-blue-900/30">
              <div className="text-[10px] text-slate-400 flex items-center gap-1 font-medium">
                <Activity className="w-3.5 h-3.5 text-purple-400" /> Packet Rate
              </div>
              <div className="text-sm font-mono font-bold text-white mt-1">
                {activeDeviceData.metrics.telemetryRate}
              </div>
            </div>
          </div>

          <div className="mt-3 p-3 rounded-xl bg-slate-950/80 border border-blue-900/40 font-mono text-xs text-blue-200">
            <span className="text-slate-400">Sensor Payload: </span>
            {activeDeviceData.metrics.reading}
          </div>
        </div>
      )}

      {/* Dual Section Grid: Your IoT Devices (Left) & Your Tokenized Assets (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Your IoT Devices (matching dashboard.html col-md-6) */}
        <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Radio className="w-4 h-4 text-blue-400" />
                Your IoT Devices
              </h3>
              <p className="text-xs text-slate-400">Registered hardware oracles & sensory telemetry nodes</p>
            </div>
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
              {iotDevices.length} Connected
            </span>
          </div>

          <div className="space-y-3">
            {iotDevices.map((device) => (
              <div
                key={device.deviceId}
                className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 hover:border-slate-700 transition"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="flex items-center space-x-2">
                      <span className="font-mono text-xs font-bold text-blue-300">
                        {device.deviceId}
                      </span>
                      <span className="h-2 w-2 rounded-full bg-emerald-400" />
                    </div>
                    <div className="text-xs text-slate-200 font-medium mt-1">
                      {device.deviceType}
                    </div>
                    <div className="text-[11px] text-slate-400 mt-0.5 truncate">
                      {device.location}
                    </div>
                  </div>

                  <button
                    onClick={() => handleFetchDeviceData(device)}
                    className="shrink-0 px-3 py-1.5 rounded-lg bg-blue-600/20 hover:bg-blue-600 text-blue-400 hover:text-white border border-blue-500/30 text-xs font-semibold transition"
                  >
                    Fetch Data
                  </button>
                </div>

                <div className="flex items-center justify-between text-[10px] text-slate-400 font-mono pt-3 mt-3 border-t border-slate-800/60">
                  <span>Battery: {device.metrics.battery}%</span>
                  <span>Signal: {device.metrics.signal} dBm</span>
                  <span>Ping: {device.lastPing}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Your Tokenized Assets (matching dashboard.html col-md-6) */}
        <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Coins className="w-4 h-4 text-purple-400" />
                Your Tokenized Assets
              </h3>
              <p className="text-xs text-slate-400">Audited real-world assets registered on the Pi Network ledger</p>
            </div>
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
              {tokenizedAssets.length} Assets
            </span>
          </div>

          <div className="space-y-3">
            {tokenizedAssets.map((asset) => (
              <div
                key={asset.assetId}
                className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 hover:border-slate-700 transition"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="flex items-center space-x-2">
                      <span className="font-mono text-xs font-bold text-purple-300">
                        {asset.assetId}
                      </span>
                      <span className="text-[10px] font-semibold px-2 py-0.2 rounded bg-purple-950 text-purple-300 border border-purple-800/40">
                        {asset.category}
                      </span>
                    </div>
                    <div className="text-xs text-white font-bold mt-1">
                      {asset.name}
                    </div>
                    <div className="text-[11px] text-slate-400 mt-0.5">
                      Owner: <span className="text-slate-300">{asset.owner}</span>
                    </div>
                  </div>

                  <div className="text-right shrink-0">
                    <div className="font-mono text-xs font-bold text-emerald-400">
                      {asset.tokenizedValue.toLocaleString()} {asset.tokenSymbol}
                    </div>
                    <div className="text-[10px] font-mono text-slate-400 mt-0.5">
                      ${(asset.valuationUsd / 1000000000).toFixed(1)}B USD
                    </div>
                  </div>
                </div>

                <div className="text-[10px] text-slate-500 pt-3 mt-3 border-t border-slate-800/60 flex items-center justify-between">
                  <span>Audit: {asset.auditDate}</span>
                  <span className="text-emerald-400 flex items-center gap-1">
                    <ShieldCheck className="w-3 h-3" /> On-Chain Verified
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Connect IoT Device Modal */}
      {isAddingDevice && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 shadow-2xl">
            <h3 className="text-base font-bold text-white mb-2">Register IoT Hardware Gateway</h3>
            <p className="text-xs text-slate-400 mb-4">
              Connect a physical or simulated sensory node to stream real-time environmental or industrial data.
            </p>
            <form onSubmit={handleDeviceSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Device Identifier</label>
                <input
                  type="text"
                  placeholder="e.g. IOT-HYDRO-STATION-701"
                  value={newDeviceId}
                  onChange={(e) => setNewDeviceId(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 font-mono focus:outline-none focus:ring-1 focus:ring-blue-500"
                  autoFocus
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Device Type</label>
                <input
                  type="text"
                  placeholder="e.g. Smart Water Flow Telemetry"
                  value={newDeviceType}
                  onChange={(e) => setNewDeviceType(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Location Coordinates / Site</label>
                <input
                  type="text"
                  placeholder="e.g. Rhone Glacier Hydrology Pod, Alps"
                  value={newDeviceLocation}
                  onChange={(e) => setNewDeviceLocation(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsAddingDevice(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!newDeviceId.trim()}
                  className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white disabled:opacity-50"
                >
                  Connect Device
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Tokenize Asset Modal */}
      {isAddingAsset && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 shadow-2xl">
            <h3 className="text-base font-bold text-white mb-2">Tokenize Real-World Asset (RWA)</h3>
            <p className="text-xs text-slate-400 mb-4">
              Mint an immutable on-chain fractional security representation backed by physical collateral.
            </p>
            <form onSubmit={handleAssetSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Asset ID</label>
                <input
                  type="text"
                  placeholder="e.g. ASSET-WIND-NORDIC-02"
                  value={newAssetId}
                  onChange={(e) => setNewAssetId(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 font-mono focus:outline-none focus:ring-1 focus:ring-purple-500"
                  autoFocus
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Asset Name</label>
                <input
                  type="text"
                  placeholder="e.g. Baltic Sea Offshore Wind Farm"
                  value={newAssetName}
                  onChange={(e) => setNewAssetName(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-purple-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Token Supply</label>
                  <input
                    type="number"
                    value={newAssetValue}
                    onChange={(e) => setNewAssetValue(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white font-mono focus:outline-none focus:ring-1 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Category</label>
                  <select
                    value={newAssetCategory}
                    onChange={(e) => setNewAssetCategory(e.target.value as TokenizedAsset['category'])}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-purple-500"
                  >
                    <option value="Renewable Energy">Renewable Energy</option>
                    <option value="Real Estate">Real Estate</option>
                    <option value="Carbon Credit">Carbon Credit</option>
                    <option value="Compute Cluster">Compute Cluster</option>
                  </select>
                </div>
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsAddingAsset(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!newAssetId.trim() || !newAssetName.trim()}
                  className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-xs font-semibold text-white disabled:opacity-50"
                >
                  Mint Asset Tokens
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
