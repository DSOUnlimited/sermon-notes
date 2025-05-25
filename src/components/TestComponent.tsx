import React from 'react';

const TestComponent: React.FC = () => {
  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-body">
              <h1 className="card-title">Test Component</h1>
              <p className="card-text">If you can see this, React is working!</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TestComponent; 