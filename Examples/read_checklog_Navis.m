function checklog = read_checklog_Navis(fltnum)
% function checklog = read_checklog_Navis(fltnum)
% reading the NAVIS BGC checklog

% for debugging
%flname = '/data1/lab/BGC/Navis/Checklogs/F1201/F1201_20200422_incoming';
%flname = ['/shared/argo/argus/1201_Mission_log.txt'];
flname = '/shared/argo/argus/1201_prebox_20210310.txt';
%flname = 'X:\argo\argus\1203_p1ebox_20210310.txt';

if exist(flname) ~=2
    disp(['Checklog file ',flname,' Not found'])
    checklog = nan;
    return
end

fid = fopen(flname);

while ~feof(fid)
    str = fgetl(fid);
    % float number and ROM version and cpuSN
    if strfind(str,'NAVIS')
        navisStr = strtrim(str);
    end
    % Park pressure
    if strfind(str,'Mk')
        parkStr = strtrim(str);
    end
    % Profile pressure
    if strfind(str,'Mj')
        profileStr = strtrim(str);
    end
    % Delay time
    if strfind(str,'Mtp')
        delayStr = strtrim(str);
    end
    % Down time
    if strfind(str,'Mtd')
        downStr = strtrim(str);
    end
    % Up time
    if strfind(str,'Mtu')
        upStr = strtrim(str);
    end
    % temperature calibration date
    if strfind(str,'temperature_1')
        tempDateStr = strtrim(str);
    end
    % conductivity calibration date
    if strfind(str,'conductivity')
        condDateStr = strtrim(str);
    end
    % pressure calibration date
    if strfind(str,'pressure S/N')
        presDateStr = strtrim(str);
    end
    % temperature and salinty serial number
    if strfind(str,'SBE 41')
        sbe41Str = strtrim(str);
    end
    % IMEI
    if strfind(str,'Modem IMEI')
        imeiStr = strtrim(str);
    end
    % oxygen model number
    if strfind(str,'LogConfig()     Model')
        oxyModelStr = strtrim(str);
    end
    % oxygen serial number
    if strfind(str,'LogConfig()     Serial')
        oxySNstr = strtrim(str);
    end
    % fluorometer
    if strfind(str,'MCOMS s')
        fluorStr = strtrim(str);
    end
    % nitrate sensor
    if strfind(str,'SUNA Serial')
        nitStr = strtrim(str);
    end
    % nitrate model
    
    % ph serial number
    if strfind(str,'pH ser')
        phStr = str;
    end
    
    % oxygen coeficients
    if strfind(str,'Sbe63LogCoef()')
        % A0
        if strfind(str,'LogCoef()       A0')
            a0Str = str;
        end
        % A1
        if strfind(str,'LogCoef()       A1')
            a1Str = str;
        end
        % A2
        if strfind(str,'LogCoef()       A2')
            a2Str = str;
        end
        % B0
        if strfind(str,'LogCoef()       B0')
            b0Str = str;
        end
        % B1
        if strfind(str,'LogCoef()       B1')
            b1Str = str;
        end
        % C0
        if strfind(str,'LogCoef()       C0')
            c0Str = str;
        end
        % C1
        if strfind(str,'C1')
            c1Str = str;
        end
        % C2
        if strfind(str,'C2')
            c2Str = str;
        end
        % E
        if strfind(str,'LogCoef()       E')
            eStr = str;
        end
        % dPhdV
        
        % D0
        if strfind(str,'SOLB0')
            d0Str = str;
        end
        % D1
        if strfind(str,'SOLB1')
            d1Str = str;
        end
        % D2
        if strfind(str,'SOLB2')
            d2Str = str;
        end
        % D3
        if strfind(str,'SOLB3')
            d3Str = str;
        end
        % D4
        if strfind(str,'SOLC0')
            d4Str = str;
        end
        
        
    end
    
    % decoder version
    
    % cpu battery SN
    
    % pump battery SN
    
end

fclose(fid)

%% extracting
% conductivity calibration date
if exist('condDateStr','var')
    checklog.condCalDate = [condDateStr(end-8:end-7),' ',sprintf('%02d',digit_month(condDateStr(end-5:end-3))),' 20',condDateStr(end-1:end)];
else
    disp('Conductivity calibration date missing')
    checklog.condCalDate = '';
end
% pressure
if exist('presDateStr','var')
    checklog.presCalDate = [presDateStr(end-8:end-7),' ',sprintf('%02d',digit_month(presDateStr(end-5:end-3))),' 20',presDateStr(end-1:end)];
    strs = split(presDateStr);
    checklog.presSN = strs{end-5};
    checklog.presSN = checklog.presSN(1:end-1);  % remove comma
else
    disp('Pressure calibration date and S/N missing')
    checklog.presCalDate = '';
    checklog.presSN = '';
end
% temperature calibration date
if exist('tempDateStr','var')
    checklog.tempCalDate = [tempDateStr(end-8:end-7),' ',sprintf('%02d',digit_month(tempDateStr(end-5:end-3))),' 20',tempDateStr(end-1:end)];
else
    disp('Temperature calibration date missing')
    checklog.tempCalDate = '';
end
% Park pressure
if exist('parkStr','var')
    strs = split(parkStr);
    checklog.parkPres = strs{end-4};
else
    disp('Park pressure missing')
    checklog.parkPres = '';
end
% Profiles pressure
if exist('profileStr','var')
    strs = split(profileStr);
    checklog.profPres = strs{end-4};
else
    disp('Profile pressure missing')
    checklog.profPres = '';
end
% Prelude delay
if exist('delayStr','var')
    strs = split(delayStr);
    checklog.delayTime = num2str(round(str2num(strs{end-4})/60));
else
    disp('Missing Prelude delay')
    checklog.delayTime = '';
end
% Down time
if exist('downStr','var')
    strs = split(downStr);
    checklog.downTime = num2str(round(str2num(strs{end-4})/60));
else
    disp('Missing down time')
    checklog.downTime = '';
end
% Up time
if exist('upStr','var')
    strs = split(upStr);
    checklog.upTime = num2str(round(str2num(strs{end-4})/60));
else
    disp('Missing up time')
    checklog.upTime = '';
end
% fluorometer
if exist('fluorStr','var')
    strs = split(fluorStr);
    fluorSN = strs{end};
    checklog.flourSN = fluorSN(2:end-1);
else
    disp('Fluorimeter serial number missing')
    checklog.flourSN = '';
end
% IMEI
if exist('imeiStr','var')
    strs = split(imeiStr);
    checklog.imei = strs{end};
else
    disp('IMEI number missing')
    checklog.imei = '';
end
% float number and ROM version and cpuSN
if exist('navisStr','var')
    strs = split(navisStr);
    checklog.floatNum = strs{end};
    checklog.rom = strs{end-2};
else
    disp('Missing Float serial number and ROM version')
    checklog.floatNum = '';
    checklog.rom = '';
end
% nitrate
if exist('nitStr','var')
    strs = split(nitStr);
    tstr = strs{end};
    i=findstr(tstr,':');
    checklog.nitSN = tstr(i+1:end);
    checklog.nitType = strs{end-4};
else
    disp('Missing Nitrate serial number and sensor type')
    checklog.nitSN = '';
    checklog.nitType = '';
end
% oxygen
if exist('oxyModelStr','var')
    strs = split(oxyModelStr);
    checklog.oxyModel = [strs{end-2},' ',strs{end-1},' ',strs{end}];
else
    disp('Missing Oxygen Model')
    checklog.oxyModel = '';
end
if exist('oxySNstr','var')
    strs = split(oxySNstr);
    checklog.oxySN = strs{end};
else
    disp('Missing Oxygen serial number')
    checklog.oxySN = '';
end
if exist('a0Str','var')
    strs = split(a0Str);
    ii = find(strcmp(strs,'='));
    checklog.oxy_a0 = strs{ii+1};
else
    disp('Missing oxygen A0 coeffienct')
    checklog.oxy_a0 = '';
end
if exist('a1Str','var')
    strs = split(a1Str);
    ii = find(strcmp(strs,'='));
    checklog.oxy_a1 = strs{ii+1};
else
    disp('Missing oxygen A1 coefficient')
    checklog.oxy_a1 = '';
end
if exist('a2Str','var')
    strs = split(a2Str);
    ii = find(strcmp(strs,'='));
    checklog.oxy_a2 = strs{ii+1};
else
    disp('Missing oxygen A2 coefficient')
    checklog.oxy_a2 = '';
end
if exist('b0Str','var')
    strs = split(b0Str);
    checklog.oxy_b0 = strs{ii+1};
else
    disp('Missing oxygen B0 coefficient')
    checklog.oxy_b0 = '';
end
if exist('b1Str','var')
    strs = split(b1Str);
    ii = find(strcmp(strs,'='));
    checklog.oxy_b1 = strs{ii+1};
else
    disp('Missing oxygen B1 coefficient')
    checklog.oxy_b1 = '';
end
if exist('c0Str','var')
    strs = split(c0Str);
    ii = find(strcmp(strs,'='));
    checklog.oxy_c0 = strs{ii+1};
else
    disp('Missing oxygen C0 coefficient')
    checklog.oxy_c0 = '';
end
if exist('c1Str','var')
    strs = split(c1Str);
    ii = find(strcmp(strs,'='));
    checklog.oxy_c1 = strs{ii+1};
else
    disp('Missing oxgyen C1 coefficient')
    checklog.oxy_c1 = '';
end
if exist('c2Str','var')
    strs = split(c2Str);
    ii = find(strcmp(strs,'='));
    checklog.oxy_c2 = strs{ii+1};
else
    disp('Missing oxygen C2 coefficient')
    checklog.oxy_c2 = '';
end
if exist('eStr','var')
    strs = split(eStr);
    ii = find(strcmp(strs,'='));
    checklog.oxy_e = strs{ii+1};
else
    disp('Missing oxygen E coefficient')
    checklog.oxy_e = '';
end
if exist('d0Str','var')
    strs = split(d0Str);
    ii = find(strcmp(strs,'='));
    checklog.oxy_d0 = strs{ii+1};
else
    disp('Missing oxygen D0 coefficient')
    checklog.oxy_d0 = '';
end
if exist('d1Str','var')
    strs = split(d1Str);
    checklog.oxy_d1 = strs{ii+1};
else
    disp('Missing oxygen D1 coefficient')
    checklog.oxy_d1 = '';
end
if exist('d2Str','var')
    strs = split(d2Str);
    ii = find(strcmp(strs,'='));
    checklog.oxy_d2 = strs{ii+1};
else
    disp('Missing oxygen D2 coefficient')
    checklog.oxy_d2 = '';
end
if exist('d3Str','var')
    strs = split(d3Str);
    ii = find(strcmp(strs,'='));
    checklog.oxy_d3 = strs{ii+1};
else
    disp('Missing oxygen D3 coefficient')
    checklog.oxy_d3 = '';
end
if exist('d4Str','var')
    strs = split(d4Str);
    ii = find(strcmp(strs,'='));
    checklog.oxy_d4 = strs{ii+1};
else
    disp('Missing oxygen D4 coefficient')
    checklog.oxy_d4  = '';
end

% pH
if exist('phStr','var')
    strs = split(phStr);
    ii = find(strcmp(strs,'number:'));
    pHSN = strs{ii+1};
    checklog.pHSN = pHSN(2:end-1);
else
    disp('Missing pH serial number')
    checklog.pHSN = '';
end
% SBE
if exist('sbe41Str','var')
    strs = split(sbe41Str);
    checklog.ctdSN = strs{end};
else
    disp('Missing SBE CTD serial number')
    checklog.ctdSN = '';
end

end


function numMon = digit_month(monStr)
% monStr - 3 letter month string
monthLtrs = ['JanFebMarAprMayJunJulAugSepOctNovDec'];
numMon = round(strfind(monthLtrs,monStr)/3+1);
end

