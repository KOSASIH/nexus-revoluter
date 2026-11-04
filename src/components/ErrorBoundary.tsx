import React from 'react';

interface Props {
  children: React.ReactNode;
  /** Changing this value (e.g. the active tab) clears a previous error. */
  resetKey?: string;
}

interface State {
  error: Error | null;
}

export class ErrorBoundary extends React.Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidUpdate(prev: Props) {
    if (this.state.error && prev.resetKey !== this.props.resetKey) {
      this.setState({ error: null });
    }
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('View crashed:', error, info.componentStack);
  }

  render() {
    if (!this.state.error) return this.props.children;
    return (
      <div role="alert" className="p-6 rounded-2xl border border-rose-800/60 bg-rose-950/30 text-rose-200 space-y-3">
        <h2 className="text-sm font-bold">This module hit an error</h2>
        <p className="text-xs text-rose-300/80 font-mono break-words">{this.state.error.message}</p>
        <button
          type="button"
          onClick={() => this.setState({ error: null })}
          className="px-3 py-1.5 rounded-lg bg-rose-800/60 hover:bg-rose-700/60 text-xs font-semibold text-white"
        >
          Try again
        </button>
      </div>
    );
  }
}
