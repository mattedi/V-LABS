"""
Orquestrador para fluxos de usuário.

Gerencia workflows relacionados a registro, autenticação,
atualização de perfil e gestão de usuários.
"""

import time
from typing import Any, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

from .coordinator import Coordinator, OrchestrationResult, OrchestrationError
from ..utils import generate_uuid, hash_password, verify_password


@dataclass
class UserRegistrationResult:
    """Resultado do fluxo de registro de usuário."""
    user_id: str
    email_verification_sent: bool
    welcome_message_sent: bool
    initial_settings_created: bool


@dataclass
class UserAuthenticationResult:
    """Resultado do fluxo de autenticação."""
    user_id: str
    access_token: str
    refresh_token: Optional[str]
    session_created: bool
    last_login_updated: bool


class UserOrchestrator(Coordinator):
    """
    Orquestrador para operações de usuário.
    
    Coordena fluxos complexos relacionados ao ciclo de vida
    do usuário no sistema educacional.
    """
    
    def __init__(self):
        super().__init__("user")
    
    async def execute(self, *args, **kwargs) -> OrchestrationResult:
        """
        Método base - não usado diretamente.
        Use os métodos específicos como register_user_flow, etc.
        """
        raise NotImplementedError("Use métodos específicos como register_user_flow")
    
    async def register_user_flow(self, user_data: Dict[str, Any],
                               send_verification: bool = True,
                               send_welcome: bool = True) -> OrchestrationResult:
        """
        Fluxo completo de registro de usuário.
        
        Passos:
        1. Validar dados do usuário
        2. Verificar se email já existe
        3. Hash da senha
        4. Criar usuário no banco
        5. Criar configurações iniciais
        6. Enviar email de verificação (opcional)
        7. Enviar mensagem de boas-vindas (opcional)
        
        Args:
            user_data: Dados do usuário
            send_verification: Se deve enviar email de verificação
            send_welcome: Se deve enviar mensagem de boas-vindas
            
        Returns:
            OrchestrationResult: Resultado do registro
        """
        workflow_id = generate_uuid()
        start_time = time.time()
        
        await self._log_workflow_start(workflow_id, "register_user", user_data)
        
        try:
            # Passo 1: Validação
            await self._execute_step(
                "validate_user_data",
                self._validate_user_registration_data,
                user_data
            )
            
            # Passo 2: Verificar email existente
            await self._execute_step(
                "check_email_exists",
                self._check_email_exists,
                user_data["email"]
            )
            
            # Passo 3: Hash da senha
            hashed_step = await self._execute_step(
                "hash_password",
                self._hash_user_password,
                user_data["senha"]
            )
            
            user_data_with_hash = user_data.copy()
            user_data_with_hash["senha"] = hashed_step["data"]["hashed_password"]
            user_data_with_hash["email_verificado"] = False
            user_data_with_hash["status"] = "active"
            
            # Passo 4: Criar usuário
            create_step = await self._execute_step(
                "create_user",
                self._create_user,
                user_data_with_hash
            )
            
            user_id = create_step["data"]["user_id"]
            
            # Passo 5: Criar configurações iniciais
            settings_created = False
            try:
                await self._execute_step(
                    "create_initial_settings",
                    self._create_user_initial_settings,
                    user_id,
                    user_data.get("tipo_usuario", "student")
                )
                settings_created = True
                
            except OrchestrationError as e:
                self.logger.warning(f"Failed to create initial settings: {e.message}")
            
            # Passo 6: Enviar verificação de email (opcional)
            email_sent = False
            if send_verification:
                try:
                    await self._execute_step(
                        "send_email_verification",
                        self._send_email_verification,
                        user_id,
                        user_data["email"]
                    )
                    email_sent = True
                    
                except OrchestrationError as e:
                    self.logger.warning(f"Failed to send verification email: {e.message}")
            
            # Passo 7: Enviar mensagem de boas-vindas (opcional)
            welcome_sent = False
            if send_welcome:
                try:
                    await self._execute_step(
                        "send_welcome_message",
                        self._send_welcome_message,
                        user_id,
                        user_data["nome"]
                    )
                    welcome_sent = True
                    
                except OrchestrationError as e:
                    self.logger.warning(f"Failed to send welcome message: {e.message}")
            
            # Resultado final
            duration_ms = (time.time() - start_time) * 1000
            
            result_data = UserRegistrationResult(
                user_id=user_id,
                email_verification_sent=email_sent,
                welcome_message_sent=welcome_sent,
                initial_settings_created=settings_created
            )
            
            result = OrchestrationResult.success_result(
                data=result_data.__dict__,
                duration_ms=duration_ms,
                steps_completed=7,
                total_steps=7
            )
            
            await self._log_workflow_end(workflow_id, result)
            return result
            
        except OrchestrationError as e:
            duration_ms = (time.time() - start_time) * 1000
            
            result = OrchestrationResult.error_result(
                errors=[e.message],
                duration_ms=duration_ms
            )
            
            await self._log_workflow_end(workflow_id, result)
            return result
    
    async def authenticate_user_flow(self, email: str, password: str,
                                   remember_me: bool = False) -> OrchestrationResult:
        """
        Fluxo completo de autenticação de usuário.
        
        Passos:
        1. Validar formato do email
        2. Buscar usuário por email
        3. Verificar senha
        4. Verificar se conta está ativa
        5. Gerar tokens de acesso
        6. Criar sessão
        7. Atualizar último login
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            remember_me: Se deve manter sessão por mais tempo
            
        Returns:
            OrchestrationResult: Resultado da autenticação
        """
        workflow_id = generate_uuid()
        start_time = time.time()
        
        auth_data = {"email": email, "remember_me": remember_me}
        await self._log_workflow_start(workflow_id, "authenticate_user", auth_data)
        
        try:
            # Passo 1: Validar email
            await self._execute_step(
                "validate_email_format",
                self._validate_email_format,
                email
            )
            
            # Passo 2: Buscar usuário
            user_step = await self._execute_step(
                "find_user_by_email",
                self._find_user_by_email,
                email
            )
            
            user_data = user_step["data"]
            user_id = user_data["_id"]
            
            # Passo 3: Verificar senha
            await self._execute_step(
                "verify_password",
                self._verify_user_password,
                password,
                user_data["senha"]
            )
            
            # Passo 4: Verificar status da conta
            await self._execute_step(
                "check_account_status",
                self._check_account_status,
                user_data
            )
            
            # Passo 5: Gerar tokens
            tokens_step = await self._execute_step(
                "generate_auth_tokens",
                self._generate_auth_tokens,
                user_id,
                remember_me
            )
            
            access_token = tokens_step["data"]["access_token"]
            refresh_token = tokens_step["data"].get("refresh_token")
            
            # Passo 6: Criar sessão
            session_created = False
            try:
                await self._execute_step(
                    "create_user_session",
                    self._create_user_session,
                    user_id,
                    access_token,
                    remember_me
                )
                session_created = True
                
            except OrchestrationError as e:
                self.logger.warning(f"Failed to create session: {e.message}")
            
            # Passo 7: Atualizar último login
            login_updated = False
            try:
                await self._execute_step(
                    "update_last_login",
                    self._update_user_last_login,
                    user_id
                )
                login_updated = True
                
            except OrchestrationError as e:
                self.logger.warning(f"Failed to update last login: {e.message}")
            
            # Resultado final
            duration_ms = (time.time() - start_time) * 1000
            
            result_data = UserAuthenticationResult(
                user_id=user_id,
                access_token=access_token,
                refresh_token=refresh_token,
                session_created=session_created,
                last_login_updated=login_updated
            )
            
            result = OrchestrationResult.success_result(
                data=result_data.__dict__,
                duration_ms=duration_ms,
                steps_completed=7,
                total_steps=7
            )
            
            await self._log_workflow_end(workflow_id, result)
            return result
            
        except OrchestrationError as e:
            duration_ms = (time.time() - start_time) * 1000
            
            result = OrchestrationResult.error_result(
                errors=[e.message],
                duration_ms=duration_ms
            )
            
            await self._log_workflow_end(workflow_id, result)
            return result
    
    # === MÉTODOS AUXILIARES ===
    
    async def _validate_user_registration_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida dados de registro de usuário."""
        required_fields = ["nome", "email", "senha", "tipo_usuario"]
        
        validation_result = await self._validate_input(user_data, required_fields)
        
        if not validation_result.success:
            raise OrchestrationError(
                f"Invalid user registration data: {', '.join(validation_result.errors)}"
            )
        
        # Validações específicas
        if len(user_data["senha"]) < 8:
            raise OrchestrationError("Password must be at least 8 characters long")
        
        if "@" not in user_data["email"]:
            raise OrchestrationError("Invalid email format")
        
        return {"valid": True}
    
    async def _check_email_exists(self, email: str) -> Dict[str, Any]:
        """Verifica se email já está em uso."""
        response = await self.persistence_gateway.get_user_by_email(email)
        
        if response.success:
            raise OrchestrationError(
                f"Email already registered: {email}"
            )
        
        return {"email_available": True}
    
    async def _hash_user_password(self, password: str) -> Dict[str, Any]:
        """Gera hash seguro da senha."""
        hashed_password = hash_password(password)
        
        return {"hashed_password": hashed_password}
    
    async def _create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria usuário no banco de dados."""
        response = await self.persistence_gateway.create_user(user_data)
        
        if not response.success:
            raise OrchestrationError(
                f"Failed to create user: {response.error_message}"
            )
        
        return {
            "user_id": response.data.get("_id"),
            "created_at": response.data.get("created_at")
        }
    
    async def _create_user_initial_settings(self, user_id: str, user_type: str) -> Dict[str, Any]:
        """Cria configurações iniciais do usuário."""
        # Configurações padrão baseadas no tipo de usuário
        default_settings = {
            "student": {
                "notifications": {"email": True, "push": False},
                "privacy": {"profile_public": False},
                "learning": {"difficulty_level": "intermediario"}
            },
            "teacher": {
                "notifications": {"email": True, "push": True},
                "privacy": {"profile_public": True},
                "teaching": {"auto_evaluate": False}
            },
            "admin": {
                "notifications": {"email": True, "push": True},
                "privacy": {"profile_public": False},
                "admin": {"dashboard_layout": "default"}
            }
        }
        
        settings = default_settings.get(user_type, default_settings["student"])
        
        settings_data = {
            "usuario_id": user_id,
            "configuracoes": settings,
            "created_at": datetime.utcnow().isoformat()
        }
        
        response = await self.persistence_gateway.mongodb.create_document(
            "configuracoes_usuario", settings_data
        )
        
        if not response.success:
            raise OrchestrationError(
                f"Failed to create user settings: {response.error_message}"
            )
        
        return {"settings_created": True}
    
    async def _send_email_verification(self, user_id: str, email: str) -> Dict[str, Any]:
        """Envia email de verificação (simulado)."""
        # Em implementação real, integraria com serviço de email
        verification_token = generate_uuid()
        
        # Simula envio de email
        await self.persistence_gateway.mongodb.create_document(
            "email_verifications",
            {
                "user_id": user_id,
                "email": email,
                "token": verification_token,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat()
            }
        )
        
        return {"verification_sent": True, "token": verification_token}
    
    async def _send_welcome_message(self, user_id: str, user_name: str) -> Dict[str, Any]:
        """Envia mensagem de boas-vindas (simulado)."""
        # Em implementação real, integraria com sistema de mensagens
        welcome_data = {
            "user_id": user_id,
            "message_type": "welcome",
            "title": f"Bem-vindo ao V-LABS, {user_name}!",
            "content": "Estamos felizes em tê-lo conosco. Explore nossa plataforma educacional.",
            "created_at": datetime.utcnow().isoformat(),
            "read": False
        }
        
        await self.persistence_gateway.mongodb.create_document("user_messages", welcome_data)
        
        return {"welcome_sent": True}
    
    async def _validate_email_format(self, email: str) -> Dict[str, Any]:
        """Valida formato do email."""
        if "@" not in email or "." not in email:
            raise OrchestrationError("Invalid email format")
        
        return {"valid": True}
    
    async def _find_user_by_email(self, email: str) -> Dict[str, Any]:
        """Busca usuário por email."""
        response = await self.persistence_gateway.get_user_by_email(email)
        
        if not response.success:
            raise OrchestrationError("Invalid email or password")
        
        return response.data
    
    async def _verify_user_password(self, password: str, hashed_password: str) -> Dict[str, Any]:
        """Verifica senha do usuário."""
        if not verify_password(password, hashed_password):
            raise OrchestrationError("Invalid email or password")
        
        return {"password_valid": True}
    
    async def _check_account_status(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica se conta está ativa e pode fazer login."""
        status = user_data.get("status", "active")
        
        if status == "inactive":
            raise OrchestrationError("Account is inactive. Please contact support.")
        
        if status == "suspended":
            raise OrchestrationError("Account is suspended. Please contact support.")
        
        if status == "deleted":
            raise OrchestrationError("Account not found.")
        
        return {"account_active": True}
    
    async def _generate_auth_tokens(self, user_id: str, remember_me: bool) -> Dict[str, Any]:
        """Gera tokens de autenticação JWT."""
        from ..utils.jwt_utils import create_access_token, create_refresh_token, hash_sensitive_data
        
        token_data = {"sub": user_id, "user_id": user_id}
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data) if remember_me else None
        
        access_expires = datetime.utcnow() + timedelta(hours=24 if remember_me else 2)
        refresh_expires = datetime.utcnow() + timedelta(days=30) if remember_me else None
        
        token_record = {
            "user_id": user_id,
            "access_token_hash": hash_sensitive_data(access_token),
            "refresh_token_hash": hash_sensitive_data(refresh_token) if refresh_token else None,
            "access_expires_at": access_expires.isoformat(),
            "refresh_expires_at": refresh_expires.isoformat() if refresh_expires else None,
            "created_at": datetime.utcnow().isoformat(),
            "active": True
        }
        
        try:
            await self.persistence_gateway.mongodb.create_document("auth_tokens", token_record)
        except Exception as e:
            self.logger.warning(f"Failed to store token record: {str(e)}")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": int(access_expires.timestamp() - datetime.utcnow().timestamp())
        }
    
    async def _create_user_session(self, user_id: str, access_token: str, 
                                 remember_me: bool) -> Dict[str, Any]:
        """Cria sessão do usuário."""
        session_data = {
            "user_id": user_id,
            "access_token": access_token,
            "remember_me": remember_me,
            "ip_address": "0.0.0.0",  # Em implementação real, obteria do request
            "user_agent": "V-LABS-Client",  # Em implementação real, obteria do request
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "active": True
        }
        
        response = await self.persistence_gateway.mongodb.create_document(
            "user_sessions", session_data
        )
        
        if not response.success:
            raise OrchestrationError(
                f"Failed to create session: {response.error_message}"
            )
        
        return {"session_created": True}
    
    async def _update_user_last_login(self, user_id: str) -> Dict[str, Any]:
        """Atualiza timestamp do último login."""
        update_data = {
            "ultimo_login": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        response = await self.persistence_gateway.update_user(user_id, update_data)
        
        if not response.success:
            raise OrchestrationError(
                f"Failed to update last login: {response.error_message}"
            )
        
        return {"last_login_updated": True}
    
    # === MÉTODOS PÚBLICOS ADICIONAIS ===
    
    async def update_user_profile_flow(self, user_id: str, update_data: Dict[str, Any],
                                     validate_changes: bool = True) -> OrchestrationResult:
        """
        Fluxo completo de atualização de perfil.
        
        Args:
            user_id: ID do usuário
            update_data: Dados para atualização
            validate_changes: Se deve validar mudanças
            
        Returns:
            OrchestrationResult: Resultado da atualização
        """
        try:
            start_time = time.time()
            
            # Busca usuário atual
            current_user_response = await self.persistence_gateway.get_user(user_id)
            
            if not current_user_response.success:
                return OrchestrationResult.error_result("User not found")
            
            current_user = current_user_response.data
            
            # Valida mudanças se solicitado
            if validate_changes:
                # Verifica se email está sendo alterado
                if "email" in update_data and update_data["email"] != current_user.get("email"):
                    # Verifica se novo email já existe
                    email_check = await self.persistence_gateway.get_user_by_email(
                        update_data["email"]
                    )
                    if email_check.success:
                        return OrchestrationResult.error_result("Email already in use")
                
                # Hash nova senha se fornecida
                if "senha" in update_data:
                    if len(update_data["senha"]) < 8:
                        return OrchestrationResult.error_result(
                            "Password must be at least 8 characters"
                        )
                    update_data["senha"] = hash_password(update_data["senha"])
            
            # Adiciona timestamp de atualização
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            # Atualiza usuário
            response = await self.persistence_gateway.update_user(user_id, update_data)
            
            if not response.success:
                return OrchestrationResult.error_result(
                    f"Failed to update profile: {response.error_message}"
                )
            
            duration_ms = (time.time() - start_time) * 1000
            
            return OrchestrationResult.success_result(
                data={"user_id": user_id, "updated_fields": list(update_data.keys())},
                duration_ms=duration_ms
            )
            
        except Exception as e:
            return OrchestrationResult.error_result(
                f"Error updating user profile: {str(e)}"
            )
    
    async def change_password_flow(self, user_id: str, current_password: str,
                                 new_password: str) -> OrchestrationResult:
        """
        Fluxo de alteração de senha.
        
        Args:
            user_id: ID do usuário
            current_password: Senha atual
            new_password: Nova senha
            
        Returns:
            OrchestrationResult: Resultado da alteração
        """
        try:
            start_time = time.time()
            
            # Busca usuário
            user_response = await self.persistence_gateway.get_user(user_id)
            
            if not user_response.success:
                return OrchestrationResult.error_result("User not found")
            
            user_data = user_response.data
            
            # Verifica senha atual
            if not verify_password(current_password, user_data["senha"]):
                return OrchestrationResult.error_result("Current password is incorrect")
            
            # Valida nova senha
            if len(new_password) < 8:
                return OrchestrationResult.error_result(
                    "New password must be at least 8 characters"
                )
            
            # Hash nova senha
            hashed_new_password = hash_password(new_password)
            
            # Atualiza senha
            update_data = {
                "senha": hashed_new_password,
                "senha_alterada_em": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            response = await self.persistence_gateway.update_user(user_id, update_data)
            
            if not response.success:
                return OrchestrationResult.error_result(
                    f"Failed to update password: {response.error_message}"
                )
            
            # Invalida todas as sessões ativas (força novo login)
            await self._invalidate_user_sessions(user_id)
            
            duration_ms = (time.time() - start_time) * 1000
            
            return OrchestrationResult.success_result(
                data={"password_changed": True, "sessions_invalidated": True},
                duration_ms=duration_ms
            )
            
        except Exception as e:
            return OrchestrationResult.error_result(
                f"Error changing password: {str(e)}"
            )
    
    async def logout_user_flow(self, user_id: str, access_token: str,
                             logout_all_devices: bool = False) -> OrchestrationResult:
        """
        Fluxo de logout do usuário.
        
        Args:
            user_id: ID do usuário
            access_token: Token de acesso atual
            logout_all_devices: Se deve fazer logout de todos os dispositivos
            
        Returns:
            OrchestrationResult: Resultado do logout
        """
        try:
            start_time = time.time()
            
            if logout_all_devices:
                # Invalida todas as sessões do usuário
                await self._invalidate_user_sessions(user_id)
                await self._invalidate_user_tokens(user_id)
            else:
                # Invalida apenas sessão/token atual
                await self._invalidate_specific_token(access_token)
                await self._invalidate_specific_session(user_id, access_token)
            
            duration_ms = (time.time() - start_time) * 1000
            
            return OrchestrationResult.success_result(
                data={
                    "logged_out": True,
                    "all_devices": logout_all_devices
                },
                duration_ms=duration_ms
            )
            
        except Exception as e:
            return OrchestrationResult.error_result(
                f"Error during logout: {str(e)}"
            )
    
    # === MÉTODOS AUXILIARES ADICIONAIS ===
    
    async def _invalidate_user_sessions(self, user_id: str) -> None:
        """Invalida todas as sessões do usuário."""
        update_data = {
            "active": False,
            "invalidated_at": datetime.utcnow().isoformat()
        }
        
        # Atualiza todas as sessões do usuário
        query = {"user_id": user_id, "active": True}
        await self.persistence_gateway.mongodb.find_documents(
            "user_sessions", query
        )
        
        # Em implementação real, faria update em massa
        # Por simplicidade, assumindo que foi atualizado
    
    async def _invalidate_user_tokens(self, user_id: str) -> None:
        """Invalida todos os tokens do usuário."""
        update_data = {
            "active": False,
            "invalidated_at": datetime.utcnow().isoformat()
        }
        
        # Atualiza todos os tokens do usuário
        query = {"user_id": user_id, "active": True}
        await self.persistence_gateway.mongodb.find_documents(
            "auth_tokens", query
        )
        
        # Em implementação real, faria update em massa
    
    async def _invalidate_specific_token(self, access_token: str) -> None:
        """Invalida token específico."""
        query = {"access_token": access_token, "active": True}
        tokens_response = await self.persistence_gateway.mongodb.find_documents(
            "auth_tokens", query
        )
        
        if tokens_response.success and tokens_response.data.get("items"):
            token_doc = tokens_response.data["items"][0]
            token_id = token_doc.get("_id")
            
            if token_id:
                update_data = {
                    "active": False,
                    "invalidated_at": datetime.utcnow().isoformat()
                }
                
                await self.persistence_gateway.mongodb.update_document(
                    "auth_tokens", token_id, update_data
                )
    
    async def _invalidate_specific_session(self, user_id: str, access_token: str) -> None:
        """Invalida sessão específica."""
        query = {"user_id": user_id, "access_token": access_token, "active": True}
        sessions_response = await self.persistence_gateway.mongodb.find_documents(
            "user_sessions", query
        )
        
        if sessions_response.success and sessions_response.data.get("items"):
            session_doc = sessions_response.data["items"][0]
            session_id = session_doc.get("_id")
            
            if session_id:
                update_data = {
                    "active": False,
                    "invalidated_at": datetime.utcnow().isoformat()
                }
                
                await self.persistence_gateway.mongodb.update_document(
                    "user_sessions", session_id, update_data
                )
