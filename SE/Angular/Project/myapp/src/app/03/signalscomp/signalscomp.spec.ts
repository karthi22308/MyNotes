import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Signalscomp } from './signalscomp';

describe('Signalscomp', () => {
  let component: Signalscomp;
  let fixture: ComponentFixture<Signalscomp>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Signalscomp]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Signalscomp);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
