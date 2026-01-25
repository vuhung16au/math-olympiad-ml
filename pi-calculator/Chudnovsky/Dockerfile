# STAGE 1: Build
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
# Build a static binary for the 'Chudnovsky' module
RUN CGO_ENABLED=0 go build -o /chudnovsky_bin

# STAGE 2: Deployment
FROM alpine:latest
WORKDIR /root/
# Copy only the compiled binary from the builder stage
COPY --from=builder /chudnovsky_bin .
# Allow the binary to be executed
RUN chmod +x ./chudnovsky_bin

ENTRYPOINT ["./chudnovsky_bin"]