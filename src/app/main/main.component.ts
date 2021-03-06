import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { OktaAuthService } from '@okta/okta-angular';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  tabOpen = false;
  openValue = '';
  isAuthenticated: boolean;

  constructor( private router: Router, private oktaAuth: OktaAuthService ) { }

  async ngOnInit() {
    this.router.navigate(['/main/home']);
    this.isAuthenticated = await this.oktaAuth.isAuthenticated();
    if (!this.isAuthenticated) {
      this.router.navigate(['login-page']);
    }
  }

  home() {
    this.router.navigate(['/main/home']);
  }

  toggleTab(id) {
    // If click on first time, open the given id
    // If click on second time, depends on whether it is the same or another id to open the tab.
    if(this.tabOpen === true) {
      console.log('id: ', id);
      if (this.openValue === id) {
        // close 
        this.tabOpen = false;       
      }
      else {
        this.setTabValue(id);
      }
    }
    else {
      // open
      this.tabOpen = true;
      this.setTabValue(id);
    }
  }

  setTabValue(id) {
    if(id === 'profile') {
      this.openValue = 'profile';
    }
    else if (id === 'notifications') {
      this.openValue = 'notifications';
    }
  }

}
