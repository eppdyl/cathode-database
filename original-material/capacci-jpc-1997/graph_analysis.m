%%% Analysis of the graph in the paper
clear all
close all
load graph_read

% Plot the raw values for A300, A500, A10000
%% A300
figure()
Xxp = A300_Vd_vs_Id_xp_1sccm(:,1);
Yxp = A300_Vd_vs_Id_xp_1sccm(:,2);
Xmodel = A300_Vd_vs_Id_model_1sccm(:,1);
Ymodel =  A300_model_1sccm(Xmodel);

plot(Xxp,Yxp,'b.--')
hold on
plot(Xmodel,Ymodel)

% Error
Ymodel =  A300_model_1sccm(Xxp);
err_A300(:,1) = Xxp;
err_A300(:,2) = 100*abs(Ymodel - Yxp)./Yxp;


%% A5000
figure()
subplot(2,1,1)
Xxp = A5000_Vd_vs_Id_xp_1sccm(:,1);
Yxp = A5000_Vd_vs_Id_xp_1sccm(:,2);
Xmodel = A5000_Vd_vs_Id_model_1sccm(:,1);
Ymodel =  A5000_model_1sccm(Xmodel);

plot(Xxp,Yxp,'b.--')
hold on
plot(Xmodel,Ymodel)

% Error
Ymodel =  A5000_model_1sccm(Xxp);
err_A5000_1sccm(:,1) = Xxp;
err_A5000_1sccm(:,2) = 100*abs(Ymodel - Yxp)./Yxp;


subplot(2,1,2)
Xxp = A5000_Vd_vs_Id_xp_2sccm(:,1);
Yxp = A5000_Vd_vs_Id_xp_2sccm(:,2);
Xmodel = A5000_Vd_vs_Id_model_2sccm(:,1);
Ymodel =  A5000_model_2sccm(Xmodel);

plot(Xxp,Yxp,'b.--')
hold on
plot(Xmodel,Ymodel)

% Error
Ymodel =  A5000_model_2sccm(Xxp);
err_A5000_2sccm(:,1) = Xxp;
err_A5000_2sccm(:,2) = 100*abs(Ymodel - Yxp)./Yxp;

%% A10000
figure()
subplot(2,2,1)
Xxp = A10000_Vd_vs_Id_xp_1sccm_05mm(:,1);
Yxp = A10000_Vd_vs_Id_xp_1sccm_05mm(:,2);
Xmodel = A10000_Vd_vs_Id_model_1sccm_05mm(:,1);
Ymodel =  A10000_model_1sccm_05mm(Xmodel);

plot(Xxp,Yxp,'b.--')
hold on
plot(Xmodel,Ymodel)

% Error
Ymodel =  A10000_model_1sccm_05mm(Xxp);
err_A10000_1sccm_05mm(:,1) = Xxp;
err_A10000_1sccm_05mm(:,2) = 100*abs(Ymodel - Yxp)./Yxp;


subplot(2,2,3)
Xxp = A10000_Vd_vs_Id_xp_2sccm_05mm(:,1);
Yxp = A10000_Vd_vs_Id_xp_2sccm_05mm(:,2);
Xmodel = A10000_Vd_vs_Id_model_2sccm_05mm(:,1);
Ymodel =  A10000_model_2sccm_05mm(Xmodel);

plot(Xxp,Yxp,'b.--')
hold on
plot(Xmodel,Ymodel)

% Error
Ymodel =  A10000_model_2sccm_05mm(Xxp);
err_A10000_2sccm_05mm(:,1) = Xxp;
err_A10000_2sccm_05mm(:,2) = 100*abs(Ymodel - Yxp)./Yxp;

subplot(2,2,2)
Xxp = A10000_Vd_vs_Id_xp_1sccm_08mm(:,1);
Yxp = A10000_Vd_vs_Id_xp_1sccm_08mm(:,2);
Xmodel = A10000_Vd_vs_Id_model_1sccm_08mm(:,1);
Ymodel =  A10000_model_1sccm_08mm(Xmodel);

plot(Xxp,Yxp,'b.--')
hold on
plot(Xmodel,Ymodel)

% Error
Ymodel =  A10000_model_1sccm_08mm(Xxp);
err_A10000_1sccm_08mm(:,1) = Xxp;
err_A10000_1sccm_08mm(:,2) = 100*abs(Ymodel - Yxp)./Yxp;


subplot(2,2,4)
Xxp = A10000_Vd_vs_Id_xp_2sccm_08mm(:,1);
Yxp = A10000_Vd_vs_Id_xp_2sccm_08mm(:,2);
Xmodel = A10000_Vd_vs_Id_model_2sccm_08mm(:,1);
Ymodel =  A10000_model_2sccm_08mm(Xmodel);

plot(Xxp,Yxp,'b.--')
hold on
plot(Xmodel,Ymodel)

% Error
Ymodel =  A10000_model_2sccm_08mm(Xxp);
err_A10000_2sccm_08mm(:,1) = Xxp;
err_A10000_2sccm_08mm(:,2) = 100*abs(Ymodel - Yxp)./Yxp;


%% Errors overall
% A300
figure()
plot(err_A300(:,1),err_A300(:,2),'b.--');
hold on
plot(err_A5000_1sccm(:,1),err_A5000_1sccm(:,2),'b.--');
hold on
plot(err_A5000_2sccm(:,1),err_A5000_2sccm(:,2),'b.--');
hold on
plot(err_A10000_1sccm_05mm(:,1),err_A10000_1sccm_05mm(:,2),'b.--');
hold on
plot(err_A10000_1sccm_08mm(:,1),err_A10000_1sccm_08mm(:,2),'b.--');
hold on
plot(err_A10000_2sccm_05mm(:,1),err_A10000_2sccm_05mm(:,2),'b.--');
hold on
plot(err_A10000_2sccm_08mm(:,1),err_A10000_2sccm_08mm(:,2),'b.--');
