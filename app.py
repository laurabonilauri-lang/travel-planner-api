import requests
from flask import redirect
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag
from pydantic import BaseModel, Field
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Configuração da API
info = Info(title="Travel Planner API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Permite requisições do front-end sem restrições de CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# 2. Configuração da Base de Dados SQLite
Base = declarative_base()


class ViagemDB(Base):
    __tablename__ = "viagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    destino = Column(String(100), nullable=False)
    data_inicio = Column(String(50), nullable=False)
    data_fim = Column(String(50), nullable=False)
    orcamento = Column(Float, nullable=False)
    bagagem = Column(String(50), nullable=False)


engine = create_engine("sqlite:///database.db", echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# 3. Tags OpenAPI3
home_tag = Tag(name="Documentação", description="Redirecionamento para Swagger")
viagem_tag = Tag(name="Viagens", description="Adição, listagem, edição e remoção de viagens")
voo_tag = Tag(name="Voos", description="Consulta de voos via API Externa pública")


# 4. Schemas Pydantic
class ViagemSchema(BaseModel):
    destino: str = Field(..., example="Miami")
    data_inicio: str = Field(..., example="2026-09-30")
    data_fim: str = Field(..., example="2026-10-07")
    orcamento: float | str = Field(..., example=10000.0)
    bagagem: str = Field(..., example="Apenas Mala de Mão")


class ViagemUpdateSchema(BaseModel):
    destino: str = Field(..., example="Miami Beach")
    data_inicio: str = Field(..., example="2026-09-30")
    data_fim: str = Field(..., example="2026-10-10")
    orcamento: float | str = Field(..., example=12000.0)
    bagagem: str = Field(..., example="Mala Despachada")


class ViagemPathSchema(BaseModel):
    viagem_id: int = Field(..., example=1, description="ID da viagem")


class ViagemViewSchema(BaseModel):
    id: int = 1
    destino: str = "Miami"
    data_inicio: str = "2026-09-30"
    data_fim: str = "2026-10-07"
    orcamento: float = 10000.0
    bagagem: str = "Apenas Mala de Mão"


class ListaViagensSchema(BaseModel):
    viagens: list[ViagemViewSchema]


class VooPathSchema(BaseModel):
    codigo_iata: str = Field(..., example="MIA", description="Código IATA do aeroporto")


class VooViewSchema(BaseModel):
    aeroporto: str = "MIA"
    status: str = "Operando"
    origem: str = "Curitiba (CWB)"
    destino: str = "Miami (MIA)"


# 5. Rotas da API

# ROTA REDIRECT (Swagger)
@app.get("/", tags=[home_tag])
def home():
    return redirect("/openapi/swagger")


# ROTA GET (Listar Viagens)
@app.get("/viagens", tags=[viagem_tag], responses={"200": ListaViagensSchema})
def get_viagens():
    session = Session()
    try:
        viagens = session.query(ViagemDB).all()
        result = [
            {
                "id": v.id,
                "destino": v.destino,
                "data_inicio": v.data_inicio,
                "data_fim": v.data_fim,
                "orcamento": v.orcamento,
                "bagagem": v.bagagem,
            }
            for v in viagens
        ]
        return {"viagens": result}, 200
    finally:
        session.close()


# ROTA POST (Cadastrar Viagem)
@app.post("/viagem", tags=[viagem_tag], responses={"201": ViagemViewSchema})
def add_viagem(body: ViagemSchema):
    session = Session()
    try:
        try:
            val_orcamento = float(body.orcamento)
        except (ValueError, TypeError):
            val_orcamento = 0.0

        nova_viagem = ViagemDB(
            destino=body.destino,
            data_inicio=str(body.data_inicio),
            data_fim=str(body.data_fim),
            orcamento=val_orcamento,
            bagagem=str(body.bagagem),
        )
        session.add(nova_viagem)
        session.commit()

        return {
            "id": nova_viagem.id,
            "destino": nova_viagem.destino,
            "data_inicio": nova_viagem.data_inicio,
            "data_fim": nova_viagem.data_fim,
            "orcamento": nova_viagem.orcamento,
            "bagagem": nova_viagem.bagagem,
        }, 201
    except Exception as e:
        session.rollback()
        return {"message": "Erro ao salvar viagem", "error": str(e)}, 400
    finally:
        session.close()


# ROTA PUT (Editar Viagem)
@app.put(
    "/viagem/<int:viagem_id>",
    tags=[viagem_tag],
    responses={"200": ViagemViewSchema},
)
def update_viagem(path: ViagemPathSchema, body: ViagemUpdateSchema):
    """Atualiza os dados de uma viagem cadastrada pelo ID (PUT)"""
    session = Session()
    try:
        viagem = session.query(ViagemDB).filter(ViagemDB.id == path.viagem_id).first()
        if not viagem:
            return {"message": "Viagem não encontrada"}, 404

        try:
            val_orcamento = float(body.orcamento)
        except (ValueError, TypeError):
            val_orcamento = viagem.orcamento

        viagem.destino = body.destino
        viagem.data_inicio = str(body.data_inicio)
        viagem.data_fim = str(body.data_fim)
        viagem.orcamento = val_orcamento
        viagem.bagagem = str(body.bagagem)

        session.commit()
        return {
            "id": viagem.id,
            "destino": viagem.destino,
            "data_inicio": viagem.data_inicio,
            "data_fim": viagem.data_fim,
            "orcamento": viagem.orcamento,
            "bagagem": viagem.bagagem,
        }, 200
    except Exception as e:
        session.rollback()
        return {"message": "Erro ao atualizar viagem", "error": str(e)}, 400
    finally:
        session.close()


# ROTA DELETE (Remover Viagem)
@app.delete("/viagem/<int:viagem_id>", tags=[viagem_tag])
def delete_viagem(path: ViagemPathSchema):
    """Deleta uma viagem cadastrada pelo ID (DELETE)"""
    session = Session()
    try:
        viagem = session.query(ViagemDB).filter(ViagemDB.id == path.viagem_id).first()
        if not viagem:
            return {"message": "Viagem não encontrada"}, 404

        session.delete(viagem)
        session.commit()
        return {"message": f"Viagem {path.viagem_id} removida com sucesso!"}, 200
    except Exception as e:
        session.rollback()
        return {"message": "Erro ao remover viagem", "error": str(e)}, 400
    finally:
        session.close()


# ROTA GET (Consulta API Externa Pública de Destinos)
@app.get(
    "/voos/<string:codigo_iata>",
    tags=[voo_tag],
    responses={"200": VooViewSchema},
)
def buscar_voos(path: VooPathSchema):
    """Consulta dados reais do destino em uma API pública externa"""
    codigo = path.codigo_iata.strip()

    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={codigo}&count=1&language=pt"
        res = requests.get(url, timeout=5)
        
        if res.status_code == 200:
            data = res.json()
            results = data.get("results")
            
            if results and len(results) > 0:
                item = results[0]
                nome = item.get("name", codigo)
                pais = item.get("country", "")
                regiao = item.get("admin1", "N/A")
                populacao = item.get("population")
                
                detalhe_local = f"{nome}, {pais}" if pais else nome
                texto_populacao = f"{populacao:,} habitantes".replace(",", ".") if populacao else "Não informada"
                
                return {
                    "aeroporto": f"Destino: {detalhe_local}",
                    "status": f"Região/Estado: {regiao} | População: {texto_populacao}",
                    "origem": "Curitiba (CWB)",
                    "destino": codigo.upper(),
                }, 200
            else:
                return {
                    "message": f"Nenhum destino localizado para o termo '{codigo}'."
                }, 404
        else:
            return {
                "message": f"Erro de resposta na API externa: status {res.status_code}."
            }, 502

    except requests.exceptions.RequestException as e:
        return {
            "message": f"Erro de conexão com a API externa: {str(e)}"
        }, 502

# 6. Execução do Servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
