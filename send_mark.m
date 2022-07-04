function y = send_mark(marca)
MARCA_DURACION=1e-3;
pportaddr = 'C020';
if exist('pportaddr','var') && ~isempty(pportaddr)
    fprintf('Connecting to parallel port 0x%s.\n', pportaddr);
    pportaddr = hex2dec(pportaddr);
    pportobj = io32;
    io32status = io32(pportobj);
    if io32status ~= 0
        error('io32 failure: could not initialise parallel port.\n');
    end
end

io64(pportobj,pportaddr, marca);
WaitSecs(MARCA_DURACION);
io64(pportobj,pportaddr,0);
display(marca)
y=1
end


