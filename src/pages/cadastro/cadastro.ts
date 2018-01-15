import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams ,ToastController} from 'ionic-angular';
import { UsuarioProvider } from "../../providers/usuario/usuario";
import { LoginPage } from "../login/login";
import { Empresa } from '../../interfaces/usuario';


/**
 * Generated class for the CadastroPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-cadastro',
  templateUrl: 'cadastro.html',
})
export class CadastroPage {

  public dados = {
    nomeUsuario: null,
    cnpj: null,
    senha: null,
    senhaConf: null,
    email: null,
    emailConf: null
  };

  constructor(public navCtrl: NavController, public navParams: NavParams, public usuarioProvider: UsuarioProvider,private toastCtrl: ToastController) {
  }

  presentToast(message:string) {
    let toast = this.toastCtrl.create({
      message: message,
      duration: 3000,
      position: 'bottom'
    });

    toast.onDidDismiss(() => {
      console.log('Dismissed toast');
    });

    toast.present();
  }
  public fazerCadastro(): void {
    // Pega as informações do usuário
    var nomeUsuario = this.dados.nomeUsuario;
    var cnpj = this.dados.cnpj;
    var senha = this.dados.senha;
    var SenhaConf = this.dados.senhaConf;

    // Compara se as senhas digitadas são correspondentes

    if (nomeUsuario==undefined ) {
      // Faz algo caso não sejam
      this.presentToast('O login é um campo obrigatório.');
      return;
    }
    //verifica se o campo não está vazio
    if (cnpj==undefined ) {
      // Faz algo caso não sejam
      this.presentToast('O CNPJ é um campo obrigatório.');
      return;
    }
    if (cnpj.length <  14 ) {
      // Faz algo caso não sejam
      this.presentToast('CNPJ inválido.');
      return;
    }
    //verifica se o campo não está vazio
    if (senha==undefined ) {
      // Faz algo caso não sejam
      this.presentToast('A senha é um campo obrigatório.');
      return;
    }
    //verifica o tamanho da senha
    if (senha.length < 6 ) {
      // Faz algo caso não sejam
      this.presentToast('A senha deve conter no minimo 6 digitos.');
      return;
    }
     //verifica se o campo não está vazio
    if (SenhaConf==undefined ) {
      // Faz algo caso não sejam
      this.presentToast('Confirmar senha é  obrigatório.');
      return;
    }


    //compara as senhas
    if (senha !== SenhaConf) {
      // Faz algo caso não sejam
      this.presentToast('As senhas não são correspondentes.');
      return;
    }

    // Pega o e-mail do usuário
    var email = this.dados.email;
    var emailConf = this.dados.emailConf;
    //verifica se o campo não está vazio
    if (email ==undefined ) {
      // Faz algo caso não sejam
      this.presentToast('O E-mail é um campo obrigatório.');
      return;
    }
    //verifica se o campo não está vazio
    if (emailConf==undefined) {
      // Faz algo caso não sejam
      this.presentToast('Confirmar E-mail é obrigatório.');
      return;
    }

    // Compara se os e-mails digitados são correspondentes
    if (email !== emailConf) {
      // Faz algo caso não sejam
      this.presentToast('Os E-mails não são correspondentes.');
      return;
    }

    // Cria o objeto usuario e o cadastro no BD
    var usuario = {
      Login: nomeUsuario,
      CNPJ: cnpj,
      Senha: senha,
      Email: email
    };

    /** ------------- AJUDA A PARTIR DE AQUI --------------- */
    var informacoes = this.usuarioProvider.validarCNPJ(usuario.CNPJ);
    console.log(informacoes);
    if (informacoes) {
      let empresa: Empresa = {
        CNPJ: usuario.CNPJ,
        Email: usuario.Email,
        Login: usuario.Login,
        Senha: usuario.Senha,
        Endereco: informacoes.endereco,
        Nome_fantasia: informacoes.nome
      };

      this.usuarioProvider.cadastrarEmpresa(empresa)
      .subscribe( response => {
        console.log(response);
        this.navCtrl.push(LoginPage, response);
      });
    } else {
      this.presentToast('Cadastro não realizado.');
    }
  }

}
