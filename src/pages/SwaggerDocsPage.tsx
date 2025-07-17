// src/pages/SwaggerDocsPage.tsx
import React from 'react';
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';

export default function SwaggerDocsPage() {
  return (
    <div className="p-4">
      <SwaggerUI url="http://localhost:8000/openapi.json" />
    </div>
  );
}
