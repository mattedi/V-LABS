import React, { useState } from 'react';

export default function ImageInput() {
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setImageUrl(url);
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleUpload} />
      {imageUrl && <img src={imageUrl} alt="Preview" className="mt-4 max-w-xs rounded" />}
    </div>
  );
}
