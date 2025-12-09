import { useEffect, useMemo, useState } from "react";
import { api, driverPortalApi } from "../lib/api";
import { Table } from "../components/Table";
import { Button } from "../components/Button";
import "../styles/login.css";

type TripPortal = {
  id: number;
  origin: string;
  destination: string;
  status: string;
  category: string;
  departure_datetime: string;
  return_datetime_expected: string;
  passengers_count: number;
  passengers_details?: { name: string; cpf: string }[];
  cargo_description?: string;
  cargo_size?: string;
  cargo_quantity?: number;
  cargo_purpose?: string;
  vehicle_id: number;
  vehicle__license_plate: string;
};

type FuelLogPortal = {
  id: number;
  filled_at: string;
  liters: string;
  fuel_station: string;
  notes?: string;
  receipt_image?: string;
  vehicle__license_plate: string;
};

export const DriverPortalPage = () => {
  const [code, setCode] = useState("");
  const [token, setToken] = useState<string | null>(localStorage.getItem("driver_portal_token"));
  const [driverName, setDriverName] = useState<string>("");
  const [trips, setTrips] = useState<TripPortal[]>([]);
  const [fuelLogs, setFuelLogs] = useState<FuelLogPortal[]>([]);
  const [fuelForm, setFuelForm] = useState<{ vehicle: number | ""; filled_at: string; liters: string; fuel_station: string; notes: string; receipt_image: File | null }>({
    vehicle: "",
    filled_at: "",
    liters: "",
    fuel_station: "",
    notes: "",
    receipt_image: null,
  });
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);

  const availableVehicles = useMemo(() => {
    const uniques = new Map<number, string>();
    trips.forEach((t) => uniques.set(t.vehicle_id, t.vehicle__license_plate));
    return Array.from(uniques.entries()).map(([id, plate]) => ({ id, plate }));
  }, [trips]);

  useEffect(() => {
    if (token) {
      loadPortalData();
    }
  }, [token]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { data } = await api.post("/drivers/portal/login/", { code });
      localStorage.setItem("driver_portal_token", data.token);
      setToken(data.token);
      setDriverName(data.driver.name);
      setError(null);
      loadPortalData();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Código inválido.");
    }
  };

  const loadPortalData = async () => {
    try {
      const tripsRes = await driverPortalApi.get<{ driver: string; trips: TripPortal[] }>("/drivers/portal/trips/");
      setDriverName(tripsRes.data.driver);
      setTrips(tripsRes.data.trips);
      const fuelRes = await driverPortalApi.get<{ logs: FuelLogPortal[] }>("/drivers/portal/fuel_logs/");
      setFuelLogs(fuelRes.data.logs);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Sessão expirada ou código inválido. Entre novamente.");
      localStorage.removeItem("driver_portal_token");
      setToken(null);
    }
  };

  const handleFuelSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!fuelForm.vehicle) {
      setError("Escolha o veículo abastecido.");
      return;
    }
    const fd = new FormData();
    fd.append("vehicle", String(fuelForm.vehicle));
    fd.append("filled_at", fuelForm.filled_at);
    fd.append("liters", fuelForm.liters);
    fd.append("fuel_station", fuelForm.fuel_station);
    if (fuelForm.notes) fd.append("notes", fuelForm.notes);
    if (fuelForm.receipt_image) fd.append("receipt_image", fuelForm.receipt_image);
    try {
      await driverPortalApi.post("/drivers/portal/fuel_logs/", fd, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFuelForm({ vehicle: fuelForm.vehicle, filled_at: "", liters: "", fuel_station: "", notes: "", receipt_image: null });
      setInfo("Abastecimento registrado.");
      loadPortalData();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro ao registrar abastecimento.");
    }
  };

  const logout = () => {
    localStorage.removeItem("driver_portal_token");
    setToken(null);
    setTrips([]);
    setFuelLogs([]);
    setDriverName("");
  };

  if (!token) {
    return (
      <div className="login" style={{ minHeight: "100vh" }}>
        <div className="login-card card">
          <h1>Acesso do motorista</h1>
          <p>Informe o código fornecido pela prefeitura para ver suas viagens e prestar contas de abastecimentos.</p>
          <form onSubmit={handleLogin} className="grid" style={{ gap: "0.75rem" }}>
            <input value={code} onChange={(e) => setCode(e.target.value.toUpperCase())} placeholder="Código do motorista" required />
            <Button type="submit">Entrar</Button>
            {error && <div className="error">{error}</div>}
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="card" style={{ margin: "1rem auto", maxWidth: 1200 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <div>
          <h2>Portal do motorista</h2>
          <p style={{ color: "var(--muted)" }}>Bem-vindo, {driverName || "motorista"}</p>
        </div>
        <Button variant="ghost" onClick={logout}>
          Sair
        </Button>
      </div>
      {error && <div className="card" style={{ color: "#f87171" }}>{error}</div>}
      {info && <div className="card" style={{ color: "#22c55e" }}>{info}</div>}
      <div className="grid" style={{ gridTemplateColumns: "1fr", gap: "1rem" }}>
        <div className="card" style={{ background: "#0f1724", border: "1px solid var(--border)" }}>
          <h3>Minhas viagens</h3>
          <Table
            columns={[
              { key: "origin", label: "Origem" },
              { key: "destination", label: "Destino" },
              { key: "category", label: "Categoria" },
              { key: "departure_datetime", label: "Saída" },
              { key: "passengers_count", label: "Passageiros" },
              { key: "vehicle__license_plate", label: "Veículo" },
            ]}
            data={trips}
          />
          {trips.some((t) => (t.passengers_details || []).length) && (
            <details style={{ marginTop: "0.5rem" }}>
              <summary>Ver lista de passageiros</summary>
              {trips.map(
                (t) =>
                  t.passengers_details?.length ? (
                    <div key={t.id} style={{ marginTop: "0.5rem" }}>
                      <strong>Viagem #{t.id}</strong>
                      <ul>
                        {t.passengers_details?.map((p, idx) => (
                          <li key={idx}>
                            {p.name} - {p.cpf}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : null
              )}
            </details>
          )}
        </div>
        <div className="card" style={{ background: "#0f1724", border: "1px solid var(--border)" }}>
          <h3>Prestação de contas de abastecimento</h3>
          <form className="grid" style={{ gap: "0.6rem" }} onSubmit={handleFuelSubmit}>
            <select value={fuelForm.vehicle} onChange={(e) => setFuelForm((f) => ({ ...f, vehicle: Number(e.target.value) }))} required>
              <option value="">Veículo</option>
              {availableVehicles.map((v) => (
                <option key={v.id} value={v.id}>
                  {v.plate}
                </option>
              ))}
            </select>
            <label>
              Data do abastecimento
              <input type="date" value={fuelForm.filled_at} onChange={(e) => setFuelForm((f) => ({ ...f, filled_at: e.target.value }))} required />
            </label>
            <input
              type="number"
              step="0.01"
              placeholder="Litros"
              value={fuelForm.liters}
              onChange={(e) => setFuelForm((f) => ({ ...f, liters: e.target.value }))}
              required
            />
            <input placeholder="Posto" value={fuelForm.fuel_station} onChange={(e) => setFuelForm((f) => ({ ...f, fuel_station: e.target.value }))} required />
            <textarea placeholder="Observações" value={fuelForm.notes} onChange={(e) => setFuelForm((f) => ({ ...f, notes: e.target.value }))} rows={2} />
            <label>
              Comprovante (foto)
              <input type="file" accept="image/*" onChange={(e) => setFuelForm((f) => ({ ...f, receipt_image: e.target.files?.[0] || null }))} />
            </label>
            <Button type="submit">Registrar abastecimento</Button>
          </form>
          <Table
            columns={[
              { key: "filled_at", label: "Data" },
              { key: "fuel_station", label: "Posto" },
              { key: "liters", label: "Litros" },
              { key: "vehicle__license_plate", label: "Veículo" },
              {
                key: "receipt_image",
                label: "Nota",
                render: (row) => (row.receipt_image ? <a href={row.receipt_image}>Ver imagem</a> : "—"),
              },
            ]}
            data={fuelLogs}
          />
        </div>
      </div>
    </div>
  );
};
