import React, { useState } from 'react';
import { Package, Plus, Trash2, Send } from 'lucide-react';

export default function ShipWiseQuoteApp() {
  const [formData, setFormData] = useState({
    clientId: '',
    profileId: '',
    shipMethod: '',
    
    // Ship To Address
    toName: '',
    toCompany: '',
    toAddress1: '',
    toAddress2: '',
    toCity: '',
    toPostalCode: '',
    toState: '',
    toCountryCode: 'US',
    toPhone: '',
    
    // Ship From Address
    fromName: '',
    fromCompany: '',
    fromAddress1: '',
    fromAddress2: '',
    fromCity: '',
    fromPostalCode: '',
    fromState: '',
    fromCountryCode: 'US',
    fromPhone: '',
    
    // Customs
    customsContentsDescription: '',
    customsOriginCountry: 'US',
    customsTag: 'Merchandise',
    customsSigner: '',
  });

  const [packages, setPackages] = useState([{
    id: 1,
    contentWeight: '',
    totalWeight: '',
    length: '',
    width: '',
    height: '',
    value: '',
    items: [{
      id: 1,
      sku: '',
      quantity: '',
      unitPrice: '',
      harmonizedCode: '',
      countryOfOrigin: 'US',
      description: '',
      declaredValue: ''
    }]
  }]);

  const [jsonOutput, setJsonOutput] = useState('');

  const addPackage = () => {
    setPackages([...packages, {
      id: packages.length + 1,
      contentWeight: '',
      totalWeight: '',
      length: '',
      width: '',
      height: '',
      value: '',
      items: [{
        id: 1,
        sku: '',
        quantity: '',
        unitPrice: '',
        harmonizedCode: '',
        countryOfOrigin: 'US',
        description: '',
        declaredValue: ''
      }]
    }]);
  };

  const removePackage = (packageIndex) => {
    if (packages.length > 1) {
      setPackages(packages.filter((_, i) => i !== packageIndex));
    }
  };

  const addItem = (packageIndex) => {
    const newPackages = [...packages];
    newPackages[packageIndex].items.push({
      id: newPackages[packageIndex].items.length + 1,
      sku: '',
      quantity: '',
      unitPrice: '',
      harmonizedCode: '',
      countryOfOrigin: 'US',
      description: '',
      declaredValue: ''
    });
    setPackages(newPackages);
  };

  const removeItem = (packageIndex, itemIndex) => {
    const newPackages = [...packages];
    if (newPackages[packageIndex].items.length > 1) {
      newPackages[packageIndex].items = newPackages[packageIndex].items.filter((_, i) => i !== itemIndex);
      setPackages(newPackages);
    }
  };

  const updatePackage = (packageIndex, field, value) => {
    const newPackages = [...packages];
    newPackages[packageIndex][field] = value;
    setPackages(newPackages);
  };

  const updateItem = (packageIndex, itemIndex, field, value) => {
    const newPackages = [...packages];
    newPackages[packageIndex].items[itemIndex][field] = value;
    setPackages(newPackages);
  };

  const generateJSON = () => {
    const isInternational = formData.toCountryCode !== formData.fromCountryCode;
    
    const output = {
      clientId: formData.clientId,
      profileId: formData.profileId,
      shipMethod: formData.shipMethod,
      to: {
        name: formData.toName,
        company: formData.toCompany,
        address1: formData.toAddress1,
        address2: formData.toAddress2,
        city: formData.toCity,
        postalCode: formData.toPostalCode,
        state: formData.toState,
        countryCode: formData.toCountryCode,
        phone: formData.toPhone
      },
      from: {
        name: formData.fromName,
        company: formData.fromCompany,
        address1: formData.fromAddress1,
        address2: formData.fromAddress2,
        city: formData.fromCity,
        postalCode: formData.fromPostalCode,
        state: formData.fromState,
        countryCode: formData.fromCountryCode,
        phone: formData.fromPhone
      },
      packages: packages.map(pkg => ({
        weightUnit: "LB",
        contentWeight: parseFloat(pkg.contentWeight) || 0,
        totalWeight: parseFloat(pkg.totalWeight) || 0,
        packaging: {
          length: parseFloat(pkg.length) || 0,
          width: parseFloat(pkg.width) || 0,
          height: parseFloat(pkg.height) || 0
        },
        value: parseFloat(pkg.value) || 0,
        ...(isInternational && {
          customs: {
            contentsDescription: formData.customsContentsDescription,
            originCountry: formData.customsOriginCountry,
            signer: formData.customsSigner,
            customsTag: formData.customsTag,
            items: pkg.items.map(item => ({
              sku: item.sku,
              description: item.description,
              qty: parseInt(item.quantity) || 0,
              value: parseFloat(item.unitPrice) || 0,
              weight: parseFloat(item.unitPrice) || 0,
              countryOfMfg: item.countryOfOrigin,
              harmCode: item.harmonizedCode
            }))
          }
        }),
        items: pkg.items.map(item => ({
          sku: item.sku,
          quantityToShip: parseInt(item.quantity) || 0,
          unitPrice: parseFloat(item.unitPrice) || 0,
          harmonizedCode: item.harmonizedCode,
          countryOfOrigin: item.countryOfOrigin,
          customsDescription: item.description,
          customsDeclaredValue: parseFloat(item.declaredValue) || 0
        }))
      }))
    };

    setJsonOutput(JSON.stringify(output, null, 2));
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(jsonOutput);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center gap-3 mb-6">
            <Package className="w-8 h-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-800">ShipWise Rate Quote Generator</h1>
          </div>

          {/* Account Information */}
          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4 text-gray-700">Account Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <input
                type="text"
                placeholder="Client ID"
                className="border rounded px-3 py-2"
                value={formData.clientId}
                onChange={(e) => setFormData({...formData, clientId: e.target.value})}
              />
              <input
                type="text"
                placeholder="Profile ID"
                className="border rounded px-3 py-2"
                value={formData.profileId}
                onChange={(e) => setFormData({...formData, profileId: e.target.value})}
              />
              <input
                type="text"
                placeholder="Ship Method"
                className="border rounded px-3 py-2"
                value={formData.shipMethod}
                onChange={(e) => setFormData({...formData, shipMethod: e.target.value})}
              />
            </div>
          </section>

          {/* Ship To Address */}
          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4 text-gray-700">Ship To Address</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Name"
                className="border rounded px-3 py-2"
                value={formData.toName}
                onChange={(e) => setFormData({...formData, toName: e.target.value})}
              />
              <input
                type="text"
                placeholder="Company"
                className="border rounded px-3 py-2"
                value={formData.toCompany}
                onChange={(e) => setFormData({...formData, toCompany: e.target.value})}
              />
              <input
                type="text"
                placeholder="Address Line 1"
                className="border rounded px-3 py-2 md:col-span-2"
                value={formData.toAddress1}
                onChange={(e) => setFormData({...formData, toAddress1: e.target.value})}
              />
              <input
                type="text"
                placeholder="Address Line 2"
                className="border rounded px-3 py-2 md:col-span-2"
                value={formData.toAddress2}
                onChange={(e) => setFormData({...formData, toAddress2: e.target.value})}
              />
              <input
                type="text"
                placeholder="City"
                className="border rounded px-3 py-2"
                value={formData.toCity}
                onChange={(e) => setFormData({...formData, toCity: e.target.value})}
              />
              <input
                type="text"
                placeholder="Postal Code"
                className="border rounded px-3 py-2"
                value={formData.toPostalCode}
                onChange={(e) => setFormData({...formData, toPostalCode: e.target.value})}
              />
              <input
                type="text"
                placeholder="State (e.g., CA)"
                className="border rounded px-3 py-2"
                value={formData.toState}
                onChange={(e) => setFormData({...formData, toState: e.target.value})}
              />
              <input
                type="text"
                placeholder="Country Code (e.g., US)"
                className="border rounded px-3 py-2"
                value={formData.toCountryCode}
                onChange={(e) => setFormData({...formData, toCountryCode: e.target.value})}
              />
              <input
                type="text"
                placeholder="Phone"
                className="border rounded px-3 py-2 md:col-span-2"
                value={formData.toPhone}
                onChange={(e) => setFormData({...formData, toPhone: e.target.value})}
              />
            </div>
          </section>

          {/* Ship From Address */}
          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4 text-gray-700">Ship From Address</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Name"
                className="border rounded px-3 py-2"
                value={formData.fromName}
                onChange={(e) => setFormData({...formData, fromName: e.target.value})}
              />
              <input
                type="text"
                placeholder="Company"
                className="border rounded px-3 py-2"
                value={formData.fromCompany}
                onChange={(e) => setFormData({...formData, fromCompany: e.target.value})}
              />
              <input
                type="text"
                placeholder="Address Line 1"
                className="border rounded px-3 py-2 md:col-span-2"
                value={formData.fromAddress1}
                onChange={(e) => setFormData({...formData, fromAddress1: e.target.value})}
              />
              <input
                type="text"
                placeholder="Address Line 2"
                className="border rounded px-3 py-2 md:col-span-2"
                value={formData.fromAddress2}
                onChange={(e) => setFormData({...formData, fromAddress2: e.target.value})}
              />
              <input
                type="text"
                placeholder="City"
                className="border rounded px-3 py-2"
                value={formData.fromCity}
                onChange={(e) => setFormData({...formData, fromCity: e.target.value})}
              />
              <input
                type="text"
                placeholder="Postal Code"
                className="border rounded px-3 py-2"
                value={formData.fromPostalCode}
                onChange={(e) => setFormData({...formData, fromPostalCode: e.target.value})}
              />
              <input
                type="text"
                placeholder="State (e.g., CA)"
                className="border rounded px-3 py-2"
                value={formData.fromState}
                onChange={(e) => setFormData({...formData, fromState: e.target.value})}
              />
              <input
                type="text"
                placeholder="Country Code (e.g., US)"
                className="border rounded px-3 py-2"
                value={formData.fromCountryCode}
                onChange={(e) => setFormData({...formData, fromCountryCode: e.target.value})}
              />
              <input
                type="text"
                placeholder="Phone"
                className="border rounded px-3 py-2 md:col-span-2"
                value={formData.fromPhone}
                onChange={(e) => setFormData({...formData, fromPhone: e.target.value})}
              />
            </div>
          </section>

          {/* Customs Information (for international) */}
          {formData.toCountryCode !== formData.fromCountryCode && (
            <section className="mb-8 bg-yellow-50 p-4 rounded">
              <h2 className="text-xl font-semibold mb-4 text-gray-700">Customs Information (International Shipment)</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="Contents Description"
                  className="border rounded px-3 py-2"
                  value={formData.customsContentsDescription}
                  onChange={(e) => setFormData({...formData, customsContentsDescription: e.target.value})}
                />
                <input
                  type="text"
                  placeholder="Origin Country Code"
                  className="border rounded px-3 py-2"
                  value={formData.customsOriginCountry}
                  onChange={(e) => setFormData({...formData, customsOriginCountry: e.target.value})}
                />
                <select
                  className="border rounded px-3 py-2"
                  value={formData.customsTag}
                  onChange={(e) => setFormData({...formData, customsTag: e.target.value})}
                >
                  <option>Merchandise</option>
                  <option>Gift</option>
                  <option>Sample</option>
                  <option>Documents</option>
                  <option>Return Goods</option>
                  <option>Donation</option>
                  <option>Dangerous Goods</option>
                  <option>Other</option>
                </select>
                <input
                  type="text"
                  placeholder="Customs Signer"
                  className="border rounded px-3 py-2"
                  value={formData.customsSigner}
                  onChange={(e) => setFormData({...formData, customsSigner: e.target.value})}
                />
              </div>
            </section>
          )}

          {/* Packages */}
          <section className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-700">Packages</h2>
              <button
                onClick={addPackage}
                className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                <Plus className="w-4 h-4" />
                Add Package
              </button>
            </div>

            {packages.map((pkg, pkgIndex) => (
              <div key={pkg.id} className="border rounded-lg p-4 mb-4 bg-gray-50">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="font-semibold text-lg">Package {pkgIndex + 1}</h3>
                  {packages.length > 1 && (
                    <button
                      onClick={() => removePackage(pkgIndex)}
                      className="text-red-600 hover:text-red-800"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  <input
                    type="number"
                    step="0.01"
                    placeholder="Content Weight (lbs)"
                    className="border rounded px-3 py-2"
                    value={pkg.contentWeight}
                    onChange={(e) => updatePackage(pkgIndex, 'contentWeight', e.target.value)}
                  />
                  <input
                    type="number"
                    step="0.01"
                    placeholder="Total Weight (lbs)"
                    className="border rounded px-3 py-2"
                    value={pkg.totalWeight}
                    onChange={(e) => updatePackage(pkgIndex, 'totalWeight', e.target.value)}
                  />
                  <input
                    type="number"
                    step="0.01"
                    placeholder="Package Value ($)"
                    className="border rounded px-3 py-2"
                    value={pkg.value}
                    onChange={(e) => updatePackage(pkgIndex, 'value', e.target.value)}
                  />
                  <input
                    type="number"
                    step="0.1"
                    placeholder="Length (in)"
                    className="border rounded px-3 py-2"
                    value={pkg.length}
                    onChange={(e) => updatePackage(pkgIndex, 'length', e.target.value)}
                  />
                  <input
                    type="number"
                    step="0.1"
                    placeholder="Width (in)"
                    className="border rounded px-3 py-2"
                    value={pkg.width}
                    onChange={(e) => updatePackage(pkgIndex, 'width', e.target.value)}
                  />
                  <input
                    type="number"
                    step="0.1"
                    placeholder="Height (in)"
                    className="border rounded px-3 py-2"
                    value={pkg.height}
                    onChange={(e) => updatePackage(pkgIndex, 'height', e.target.value)}
                  />
                </div>

                {/* Items in Package */}
                <div className="ml-4">
                  <div className="flex justify-between items-center mb-3">
                    <h4 className="font-semibold">Items</h4>
                    <button
                      onClick={() => addItem(pkgIndex)}
                      className="flex items-center gap-1 bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700"
                    >
                      <Plus className="w-3 h-3" />
                      Add Item
                    </button>
                  </div>

                  {pkg.items.map((item, itemIndex) => (
                    <div key={item.id} className="border rounded p-3 mb-3 bg-white">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium">Item {itemIndex + 1}</span>
                        {pkg.items.length > 1 && (
                          <button
                            onClick={() => removeItem(pkgIndex, itemIndex)}
                            className="text-red-600 hover:text-red-800"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <input
                          type="text"
                          placeholder="SKU"
                          className="border rounded px-3 py-2 text-sm"
                          value={item.sku}
                          onChange={(e) => updateItem(pkgIndex, itemIndex, 'sku', e.target.value)}
                        />
                        <input
                          type="number"
                          placeholder="Quantity"
                          className="border rounded px-3 py-2 text-sm"
                          value={item.quantity}
                          onChange={(e) => updateItem(pkgIndex, itemIndex, 'quantity', e.target.value)}
                        />
                        <input
                          type="number"
                          step="0.01"
                          placeholder="Unit Price ($)"
                          className="border rounded px-3 py-2 text-sm"
                          value={item.unitPrice}
                          onChange={(e) => updateItem(pkgIndex, itemIndex, 'unitPrice', e.target.value)}
                        />
                        <input
                          type="text"
                          placeholder="HS Code"
                          className="border rounded px-3 py-2 text-sm"
                          value={item.harmonizedCode}
                          onChange={(e) => updateItem(pkgIndex, itemIndex, 'harmonizedCode', e.target.value)}
                        />
                        <input
                          type="text"
                          placeholder="Country of Origin"
                          className="border rounded px-3 py-2 text-sm"
                          value={item.countryOfOrigin}
                          onChange={(e) => updateItem(pkgIndex, itemIndex, 'countryOfOrigin', e.target.value)}
                        />
                        <input
                          type="number"
                          step="0.01"
                          placeholder="Declared Value ($)"
                          className="border rounded px-3 py-2 text-sm"
                          value={item.declaredValue}
                          onChange={(e) => updateItem(pkgIndex, itemIndex, 'declaredValue', e.target.value)}
                        />
                        <input
                          type="text"
                          placeholder="Description"
                          className="border rounded px-3 py-2 text-sm md:col-span-2"
                          value={item.description}
                          onChange={(e) => updateItem(pkgIndex, itemIndex, 'description', e.target.value)}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </section>

          <button
            onClick={generateJSON}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 flex items-center justify-center gap-2"
          >
            <Send className="w-5 h-5" />
            Generate JSON
          </button>
        </div>

        {/* JSON Output */}
        {jsonOutput && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-700">Generated JSON</h2>
              <button
                onClick={copyToClipboard}
                className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
              >
                Copy to Clipboard
              </button>
            </div>
            <pre className="bg-gray-900 text-green-400 p-4 rounded overflow-x-auto text-sm">
              {jsonOutput}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}