'use client';

import { useState } from 'react';

interface Wallet {
  id: string;
  name: string;
  type: 'hot' | 'cold' | 'multi-sig';
  balance: number;
  currency: string;
  value: number;
}

interface Transaction {
  id: string;
  type: 'send' | 'receive' | 'swap' | 'stake';
  amount: number;
  currency: string;
  value: number;
  status: 'confirmed' | 'pending' | 'failed';
  to?: string;
  from?: string;
  time: string;
}

const wallets: Wallet[] = [
  { id: 'w1', name: 'Main Wallet', type: 'hot', balance: 12450, currency: 'USDC', value: 12450 },
  { id: 'w2', name: 'Agent Fund', type: 'multi-sig', balance: 50000, currency: 'USDC', value: 50000 },
  { id: 'w3', name: 'Cold Storage', type: 'cold', balance: 250000, currency: 'USDC', value: 250000 },
];

const transactions: Transaction[] = [
  { id: 't1', type: 'send', amount: 500, currency: 'USDC', value: 500, status: 'confirmed', to: '0x742d...3f2a', time: '2 hours ago' },
  { id: 't2', type: 'receive', amount: 2500, currency: 'USDC', value: 2500, status: 'confirmed', from: '0x8a3d...1c4b', time: '5 hours ago' },
  { id: 't3', type: 'swap', amount: 1000, currency: 'ETH', value: 2400, status: 'confirmed', time: '1 day ago' },
  { id: 't4', type: 'stake', amount: 10000, currency: 'USDC', value: 10000, status: 'pending', time: '2 days ago' },
  { id: 't5', type: 'send', amount: 200, currency: 'USDC', value: 200, status: 'failed', to: '0x1234...abcd', time: '3 days ago' },
];

const defiPositions = [
  { protocol: 'Aave', asset: 'USDC', deposited: 25000, apy: 4.2, earned: 456, color: '#2EC8FE' },
  { protocol: 'Compound', asset: 'USDC', deposited: 15000, apy: 3.8, earned: 234, color: '#00D395' },
  { protocol: 'Uniswap', asset: 'ETH-USDC', deposited: 12000, apy: 12.5, earned: 890, color: '#FF007A' },
];

export default function WalletPage() {
  const [activeTab, setActiveTab] = useState<'wallets' | 'activity' | 'defi'>('wallets');
  
  const totalValue = wallets.reduce((a, w) => a + w.value, 0);
  
  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>AgentWallet</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Multi-chain crypto & DeFi wallet for AI agents</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button style={{ background: '#238636', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 8, fontSize: 13, cursor: 'pointer' }}>
            + Connect Wallet
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {(['wallets', 'activity', 'defi'] as const).map(t => (
          <button
            key={t}
            onClick={() => setActiveTab(t)}
            style={{
              background: activeTab === t ? '#1F2937' : 'transparent',
              color: activeTab === t ? '#fff' : '#6B7280',
              border: 'none',
              padding: '10px 20px',
              borderRadius: 8,
              fontSize: 13,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {t === 'wallets' ? 'Wallets' : t === 'activity' ? 'Activity' : 'DeFi'}
          </button>
        ))}
      </div>

      {activeTab === 'wallets' ? (
        <>
          {/* Total Balance */}
          <div style={{ background: 'linear-gradient(135deg, #667EEA 0%, #764BA2 100%)', borderRadius: 16, padding: 32, marginBottom: 24 }}>
            <div style={{ fontSize: 14, opacity: 0.8, marginBottom: 8 }}>Total Portfolio Value</div>
            <div style={{ fontSize: 48, fontWeight: 700 }}>${totalValue.toLocaleString()}</div>
            <div style={{ fontSize: 14, marginTop: 16, opacity: 0.8 }}>≈ {totalValue.toLocaleString()} USDC</div>
          </div>

          {/* Wallets */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
            {wallets.map(wallet => (
              <div key={wallet.id} style={{ background: '#1F2937', borderRadius: 12, padding: 20 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
                  <div>
                    <div style={{ fontSize: 16, fontWeight: 600 }}>{wallet.name}</div>
                    <div style={{ fontSize: 11, color: '#6B7280', textTransform: 'capitalize' }}>{wallet.type} Wallet</div>
                  </div>
                  <span style={{ 
                    background: wallet.type === 'hot' ? '#238636' : wallet.type === 'cold' ? '#1F2937' : '#F59E0B20',
                    color: wallet.type === 'hot' ? '#fff' : wallet.type === 'cold' ? '#6B7280' : '#F59E0B',
                    padding: '4px 8px',
                    borderRadius: 4,
                    fontSize: 10,
                    textTransform: 'uppercase',
                    fontWeight: 500,
                  }}>
                    {wallet.type}
                  </span>
                </div>
                <div style={{ fontSize: 28, fontWeight: 600, marginBottom: 4 }}>${wallet.balance.toLocaleString()}</div>
                <div style={{ fontSize: 12, color: '#6B7280' }}>{wallet.currency}</div>
                <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
                  <button style={{ flex: 1, background: '#374151', color: '#fff', border: 'none', padding: '8px 0', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
                    Send
                  </button>
                  <button style={{ flex: 1, background: '#374151', color: '#fff', border: 'none', padding: '8px 0', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
                    Receive
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Quick Actions */}
          <div style={{ marginTop: 24, padding: 20, background: '#1F2937', borderRadius: 12 }}>
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Quick Actions</h3>
            <div style={{ display: 'flex', gap: 12 }}>
              {['Buy Crypto', 'Swap', 'Bridge', 'Stake'].map(action => (
                <button key={action} style={{ background: '#374151', color: '#fff', border: 'none', padding: '12px 20px', borderRadius: 8, fontSize: 13, cursor: 'pointer', flex: 1 }}>
                  {action}
                </button>
              ))}
            </div>
          </div>
        </>
      ) : activeTab === 'activity' ? (
        <div style={{ background: '#1F2937', borderRadius: 12, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#111827' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>TYPE</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>AMOUNT</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>VALUE</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>DETAILS</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>TIME</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map(t => (
                <tr key={t.id} style={{ borderTop: '1px solid #374151' }}>
                  <td style={{ padding: '14px 16px', fontSize: 12, textTransform: 'uppercase', fontWeight: 500 }}>
                    {t.type === 'send' ? '📤 Send' : t.type === 'receive' ? '📥 Receive' : t.type === 'swap' ? '🔄 Swap' : '📊 Stake'}
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{t.amount.toLocaleString()} {t.currency}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontWeight: 600 }}>${t.value.toLocaleString()}</td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{ 
                      color: t.status === 'confirmed' ? '#10B981' : t.status === 'pending' ? '#F59E0B' : '#DA1E28',
                      fontSize: 12,
                      fontWeight: 500,
                    }}>
                      {t.status === 'confirmed' ? '● Confirmed' : t.status === 'pending' ? '⏳ Pending' : '✗ Failed'}
                    </span>
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280', fontFamily: 'monospace' }}>
                    {t.type === 'send' ? `→ ${t.to}` : t.type === 'receive' ? `← ${t.from}` : t.type === 'swap' ? 'ETH → USDC' : 'Locked'}
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{t.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {defiPositions.map(pos => (
            <div key={pos.protocol} style={{ background: '#1F2937', borderRadius: 12, padding: 20 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                <div style={{ width: 40, height: 40, borderRadius: 10, background: pos.color, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 18 }}>
                  {pos.protocol.charAt(0)}
                </div>
                <div>
                  <div style={{ fontSize: 16, fontWeight: 600 }}>{pos.protocol}</div>
                  <div style={{ fontSize: 12, color: '#6B7280' }}>{pos.asset}</div>
                </div>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12, marginBottom: 16 }}>
                <div>
                  <div style={{ fontSize: 11, color: '#6B7280' }}>Deposited</div>
                  <div style={{ fontSize: 18, fontWeight: 600 }}>${pos.deposited.toLocaleString()}</div>
                </div>
                <div>
                  <div style={{ fontSize: 11, color: '#6B7280' }}>APY</div>
                  <div style={{ fontSize: 18, fontWeight: 600, color: '#10B981' }}>{pos.apy}%</div>
                </div>
              </div>
              <div style={{ paddingTop: 16, borderTop: '1px solid #374151' }}>
                <div style={{ fontSize: 11, color: '#6B7280', marginBottom: 4 }}>Total Earned</div>
                <div style={{ fontSize: 24, fontWeight: 600, color: '#10B981' }}>+${pos.earned}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}