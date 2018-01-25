import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, ToastController} from 'ionic-angular';
import { UsuarioProvider } from "../../providers/usuario/usuario";
import { Pacote } from "../../interfaces/ordem-de-servico";
import { HomePage } from "../home/home";
import { SessionProvider } from '../../providers/session/session';
import { PacoteProvider } from '../../providers/pacote/pacote'
import { ClienteProvider } from '../../providers/cliente/cliente';

/**
 * Generated class for the CadastroPacote2Page page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-cadastro-pacote2',
  templateUrl: 'cadastro-pacote2.html',
})
export class CadastroPacote2Page {

  public dados = {
    altura: '',
    largura: '',
    comprimento: '',
    peso: ''
  };

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    public usuarioProvider: UsuarioProvider,
    private toastCtrl: ToastController,
    private pacoteProvider: PacoteProvider,
    private clienteProvider: ClienteProvider) {  }

  /**
   * Realiza o cadastro do pacote
   * no banco de dados.
   *
   * Feito por: Augusto Paiva, 10/12/2017
   */

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

  public cadastrarPacote(): void{
    var peso = this.dados.peso;
    var altura = this.dados.altura;
    var largura = this.dados.largura;
    var comprimento = this.dados.comprimento;

    if (!peso ) {
      this.presentToast('O peso é um campo obrigatório.');
      return;
    }
    if (!altura ) {
      this.presentToast('A altura é um campo obrigatório.');
      return;
    }
    if (!largura ) {
      this.presentToast('A largura é um campo obrigatório.');
      return;
    }
    if (!comprimento ) {
      this.presentToast('O comprimento é um campo obrigatório.');
      return;
    }

    var id_endereco_destino;
    let id_cliente = this.navParams.get('cliente');
    this.clienteProvider.pegarCliente(id_cliente).subscribe(response => {
      console.log(response);
      id_endereco_destino = response.addresses[0].id;
    }, error => console.log('Erro ao pegar cliente: ' + error));

    let pacote: Pacote = {
       width: +largura,
       height: +altura,
       length: +comprimento,
       weight: +peso,
       volume: +largura * +altura * +comprimento,
       id_address_start: SessionProvider.getUser().Endereco.id,
       id_address_destiny: id_endereco_destino,
       id_client: id_cliente,
       shipped: false,
       received: false,
       static_location: '',
       status: 'em fila de coleta',
       id_company: SessionProvider.getUser().id
     };
     console.log(pacote);
    
     this.pacoteProvider.cadastrarPacote(pacote, (response) => {
       console.log(response);
       this.navCtrl.push(HomePage, response);
     });
  }

}
