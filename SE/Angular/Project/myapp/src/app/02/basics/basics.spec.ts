import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Basics } from './basics';

describe('Basics', () => {
  let component: Basics;
  let fixture: ComponentFixture<Basics>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Basics]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Basics);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
